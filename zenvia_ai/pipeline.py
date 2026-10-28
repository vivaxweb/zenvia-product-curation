"""
Core Multimodal Vision Classification Pipeline for Zenvia AI.
"""

import time
import json
import re
import requests
from typing import Optional, Dict, Any, List

from .config import Config, setup_logger
from .taxonomy import (
    VALID_VIBES,
    VALID_OCCASIONS,
    get_subcategories_for_category,
    validate_vibe_tags,
    sanitize_subcategory,
    sanitize_occasion,
)
from .models import ProductItem, ClassificationResult

logger = setup_logger("zenvia_ai.pipeline")


class VibeClassificationPipeline:
    """Multimodal vision-language pipeline for classifying apparel vibes."""

    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id or Config.DEFAULT_MODEL
        self.headers = Config.get_headers()
        self.base_url = Config.BASE_URL

    def build_multimodal_payload(self, item: ProductItem) -> Dict[str, Any]:
        """Construct the OpenAI-compatible multimodal chat payload."""
        allowed_subcats = get_subcategories_for_category(item.category)

        prompt_text = (
            f"You are Zenvia's expert Gen Z fashion curator (India market, target audience: 16-26 years).\n"
            f"Analyze the garment photography and metadata below, then assign the correct aesthetic taxonomy.\n\n"
            f"PRODUCT DETAILS:\n"
            f"- Title: {item.name}\n"
            f"- Category: {item.category}\n"
            f"- Description: {item.description or 'Quality apparel garment'}\n\n"
            f"PERMISSIBLE CHOICES:\n"
            f"- Aesthetic Vibes (pick 1-2): {', '.join(VALID_VIBES)}\n"
            f"- Subcategory (pick exactly 1): {', '.join(allowed_subcats)}\n"
            f"- Occasion (pick exactly 1): {', '.join(VALID_OCCASIONS)}\n\n"
            f"TASK:\n"
            f"Inspect visual cues (silhouette, drop shoulder, graphic lettering, wash, texture, fit, palette).\n"
            f"Return ONLY a valid JSON object strictly matching this schema:\n"
            f'{{"vibeTags": ["streetwear"], "subcategory": "t-shirts", "occasion": "casual", "confidence": 0.95, "visualNote": "concise observation of image cues"}}'
        )

        content: List[Dict[str, Any]] = [{"type": "text", "text": prompt_text}]

        # Inject image modality if a valid URL is present
        if item.main_image and str(item.main_image).strip().startswith("http"):
            content.append({
                "type": "image_url",
                "image_url": {"url": str(item.main_image).strip()}
            })

        return {
            "model": self.model_id,
            "messages": [{"role": "user", "content": content}],
            "temperature": Config.TEMPERATURE,
            "max_tokens": Config.MAX_TOKENS,
        }

    def _extract_json_from_raw(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON from raw text or reasoning tokens."""
        if not raw_text or not isinstance(raw_text, str):
            return None

        # Try direct load
        try:
            return json.loads(raw_text.strip())
        except Exception:
            pass

        # Try markdown code block extraction
        code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if code_block:
            try:
                return json.loads(code_block.group(1).strip())
            except Exception:
                pass

        # Regex greedy object search
        match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0).strip())
            except Exception:
                pass

        return None

    def classify(self, item: ProductItem) -> ClassificationResult:
        """
        Classify a single product item with automatic retries and exponential backoff.
        """
        payload = self.build_multimodal_payload(item)
        start_time = time.time()
        last_error = ""

        for attempt in range(Config.MAX_RETRIES):
            try:
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=Config.REQUEST_TIMEOUT,
                )

                if response.status_code == 200:
                    data = response.json()
                    choice = data.get("choices", [{}])[0]
                    message = choice.get("message", {})
                    raw_content = message.get("content") or message.get("reasoning") or ""
                    tokens_used = data.get("usage", {}).get("total_tokens", 0)
                    elapsed = round(time.time() - start_time, 2)

                    parsed_json = self._extract_json_from_raw(raw_content)
                    if parsed_json:
                        raw_vibes = parsed_json.get("vibeTags", [])
                        if isinstance(raw_vibes, str):
                            raw_vibes = [v.strip() for v in raw_vibes.split(",")]
                        elif not isinstance(raw_vibes, list):
                            raw_vibes = [str(raw_vibes)]

                        valid_vibes, _ = validate_vibe_tags(raw_vibes)
                        if not valid_vibes:
                            valid_vibes = ["streetwear"] if item.category == "men" else ["cleangirl"]

                        final_subcat = sanitize_subcategory(parsed_json.get("subcategory", ""), item.category)
                        final_occasion = sanitize_occasion(parsed_json.get("occasion", "casual"))
                        conf = float(parsed_json.get("confidence", 0.90))

                        return ClassificationResult(
                            vibe_tags=valid_vibes,
                            subcategory=final_subcat,
                            occasion=final_occasion,
                            confidence=min(max(conf, 0.0), 1.0),
                            visual_note=str(parsed_json.get("visualNote", "")),
                            tokens_used=tokens_used,
                            latency_seconds=elapsed,
                            status="ok",
                            raw_response=raw_content[:200],
                        )
                    else:
                        logger.warning(f"Could not parse JSON on attempt {attempt+1}. Raw: {raw_content[:100]}")
                        last_error = "json_parse_failure"

                elif response.status_code == 429:
                    wait_time = Config.RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Rate limited (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    last_error = "rate_limited_429"
                else:
                    logger.error(f"API Error {response.status_code}: {response.text[:150]}")
                    last_error = f"http_{response.status_code}"

            except Exception as exc:
                logger.error(f"Network exception on attempt {attempt+1}: {exc}")
                last_error = f"exception_{str(exc)[:30]}"
                time.sleep(Config.RETRY_DELAY)

        # Fallback heuristic if all attempts fail
        elapsed = round(time.time() - start_time, 2)
        fallback_vibe = item.manual_vibes or ("streetwear" if item.category == "men" else "aesthetic")
        fallback_subcat = sanitize_subcategory(item.manual_subcategory or "", item.category)

        return ClassificationResult(
            vibe_tags=[v.strip() for v in fallback_vibe.split(",") if v.strip()],
            subcategory=fallback_subcat,
            occasion="casual",
            confidence=0.50,
            visual_note="Fallback heuristics applied due to API rate limit",
            tokens_used=0,
            latency_seconds=elapsed,
            status=f"fallback: {last_error}",
        )

"""
Unit Tests for Vibe Classification Pipeline and Extraction Logic.
"""

from unittest.mock import patch, MagicMock
from zenvia_ai.models import ProductItem
from zenvia_ai.pipeline import VibeClassificationPipeline


def test_build_multimodal_payload_with_and_without_image():
    """Verify payload generation for text-only vs image-inclusive items."""
    pipeline = VibeClassificationPipeline()

    item_with_img = ProductItem(
        name="Oversized Street Tee",
        main_image="https://example.com/tee.jpg",
    )
    payload_with_img = pipeline.build_multimodal_payload(item_with_img)
    content = payload_with_img["messages"][0]["content"]
    assert len(content) == 2
    assert content[0]["type"] == "text"
    assert content[1]["type"] == "image_url"

    item_text_only = ProductItem(
        name="Linen Casual Shirt",
        main_image="",
    )
    payload_text_only = pipeline.build_multimodal_payload(item_text_only)
    content_text = payload_text_only["messages"][0]["content"]
    assert len(content_text) == 1
    assert content_text[0]["type"] == "text"


def test_extract_json_from_raw():
    """Verify resilient extraction from clean, markdown, and embedded JSON."""
    pipeline = VibeClassificationPipeline()

    # Clean JSON
    res1 = pipeline._extract_json_from_raw('{"vibeTags": ["streetwear"]}')
    assert res1 == {"vibeTags": ["streetwear"]}

    # Markdown Code Block
    res2 = pipeline._extract_json_from_raw('```json\n{"vibeTags": ["oldmoney"]}\n```')
    assert res2 == {"vibeTags": ["oldmoney"]}

    # Embedded in conversational filler
    res3 = pipeline._extract_json_from_raw('Here is the parsed output: {"vibeTags": ["y2k"]}. Thank you!')
    assert res3 == {"vibeTags": ["y2k"]}

    # Invalid input
    assert pipeline._extract_json_from_raw(None) is None
    assert pipeline._extract_json_from_raw("plain text without brackets") is None


def test_classify_mocked_success():
    """Verify classify execution with a mocked successful response."""
    pipeline = VibeClassificationPipeline()
    item = ProductItem(name="Varsity Bomber Jacket", category="men")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": '{"vibeTags": ["streetwear", "retro"], "subcategory": "bomber-jackets", "occasion": "casual", "confidence": 0.98, "visualNote": "vintage wool leather sleeve"}'
                }
            }
        ],
        "usage": {"total_tokens": 450},
    }

    with patch("requests.post", return_value=mock_resp):
        result = pipeline.classify(item)
        assert result.status == "ok"
        assert "streetwear" in result.vibe_tags
        assert result.subcategory == "bomber-jackets"
        assert result.confidence == 0.98

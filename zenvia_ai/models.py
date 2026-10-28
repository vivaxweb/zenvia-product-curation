"""
Data Models and Schemas for Zenvia AI Pipeline.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ProductItem(BaseModel):
    """Normalized schema for raw incoming catalog items."""

    name: str = Field(..., description="Product title or heading")
    price: Optional[float] = Field(default=0.0, description="Original MRP in INR")
    discounted_price: Optional[float] = Field(default=0.0, description="Discounted selling price in INR")
    description: Optional[str] = Field(default="", description="Product description or seller notes")
    category: str = Field(default="men", description="Root category: men, women, all")
    main_image: Optional[str] = Field(default="", description="Primary product image URL")
    manual_vibes: Optional[str] = Field(default="", description="Pre-existing manual vibe tag if present")
    manual_subcategory: Optional[str] = Field(default="", description="Pre-existing manual subcategory")
    source: Optional[str] = Field(default="unknown", description="Marketplace source: amazon, flipkart, myntra, meesho")
    redirect_link: Optional[str] = Field(default="", description="Affiliate product URL")
    rating: Optional[float] = Field(default=0.0, description="Customer star rating (>=3.5)")

    @field_validator("category")
    @classmethod
    def clean_category(cls, v: str) -> str:
        clean = (v or "men").strip().lower()
        return clean if clean in ("men", "women", "all") else "men"


class ClassificationResult(BaseModel):
    """Structured response produced by the multimodal vision model."""

    vibe_tags: List[str] = Field(default_factory=list, description="Classified aesthetic vibes")
    subcategory: str = Field(default="", description="Classified garment subcategory")
    occasion: str = Field(default="casual", description="Target wearing occasion")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Model classification confidence score")
    visual_note: str = Field(default="", description="Visual features observed in product photography")
    tokens_used: int = Field(default=0, description="Total API token consumption")
    latency_seconds: float = Field(default=0.0, description="Execution time in seconds")
    status: str = Field(default="ok", description="Status indicator: ok, fallback, error")
    raw_response: Optional[str] = Field(default="", description="Raw response text for debugging")

    @property
    def vibe_string(self) -> str:
        """Comma-separated representation of vibe tags."""
        return ", ".join(self.vibe_tags)


class EvaluationMetrics(BaseModel):
    """Evaluation summary metrics comparing AI against ground truth curation."""

    total_evaluated: int = Field(default=0, description="Total products evaluated")
    exact_match_count: int = Field(default=0, description="Exact vibe set matches")
    partial_match_count: int = Field(default=0, description="At least one shared vibe tag")
    subcategory_match_count: int = Field(default=0, description="Exact subcategory matches")
    average_confidence: float = Field(default=0.0, description="Mean prediction confidence")
    average_latency: float = Field(default=0.0, description="Mean latency per item in seconds")
    agreement_rate: float = Field(default=0.0, description="Overall human-AI agreement percentage")
    vibe_distribution: Dict[str, int] = Field(default_factory=dict, description="Counts per vibe tag")
    occasion_distribution: Dict[str, int] = Field(default_factory=dict, description="Counts per occasion")

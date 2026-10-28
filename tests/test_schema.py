"""
Unit Tests for Pydantic Models and Data Serialization.
"""

import pytest
from zenvia_ai.models import ProductItem, ClassificationResult, EvaluationMetrics


def test_product_item_default_initialization():
    """Verify that ProductItem handles minimal inputs and cleans categories."""
    item = ProductItem(name="Vintage Graphic Tee")
    assert item.name == "Vintage Graphic Tee"
    assert item.category == "men"
    assert item.price == 0.0

    # Category cleaning
    item2 = ProductItem(name="Satin Slip Dress", category="WOMEN")
    assert item2.category == "women"

    item3 = ProductItem(name="Unisex Belt", category="other")
    assert item3.category == "men"


def test_classification_result_property_and_defaults():
    """Verify ClassificationResult properties and constraints."""
    result = ClassificationResult(
        vibe_tags=["streetwear", "retro"],
        subcategory="t-shirts",
        confidence=0.95,
        visual_note="Distressed wash print",
    )
    assert result.vibe_string == "streetwear, retro"
    assert result.status == "ok"
    assert result.confidence == 0.95


def test_evaluation_metrics_initialization():
    """Verify EvaluationMetrics schema serialization."""
    metrics = EvaluationMetrics(
        total_evaluated=10,
        exact_match_count=8,
        partial_match_count=10,
        agreement_rate=100.0,
        average_confidence=0.94,
    )
    dumped = metrics.model_dump()
    assert dumped["total_evaluated"] == 10
    assert dumped["agreement_rate"] == 100.0

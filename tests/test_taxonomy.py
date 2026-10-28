"""
Unit Tests for Zenvia Taxonomy and Sanitization Functions.
"""

from zenvia_ai.taxonomy import (
    VALID_VIBES,
    VALID_SUBCATEGORIES_MEN,
    VALID_SUBCATEGORIES_WOMEN,
    VALID_OCCASIONS,
    validate_vibe_tags,
    sanitize_subcategory,
    sanitize_occasion,
    get_subcategories_for_category,
)


def test_taxonomy_collections_not_empty():
    """Verify that all core taxonomy collections contain standard values."""
    assert len(VALID_VIBES) >= 20
    assert len(VALID_SUBCATEGORIES_MEN) >= 15
    assert len(VALID_SUBCATEGORIES_WOMEN) >= 15
    assert len(VALID_OCCASIONS) >= 5


def test_validate_vibe_tags_filters_correctly():
    """Verify that valid vibes are kept and invalid tags are segregated."""
    input_tags = ["streetwear", "oldmoney", "invalid_fake_tag", "  y2k  "]
    valid, invalid = validate_vibe_tags(input_tags)

    assert "streetwear" in valid
    assert "oldmoney" in valid
    assert "y2k" in valid
    assert "invalid_fake_tag" in invalid


def test_sanitize_subcategory_resolution():
    """Verify subcategory resolution and fallback logic."""
    assert sanitize_subcategory("t-shirts", "men") == "t-shirts"
    assert sanitize_subcategory("hoodie", "men") == "hoodies"
    assert sanitize_subcategory("dresses", "women") == "dresses"
    assert sanitize_subcategory("", "men") in VALID_SUBCATEGORIES_MEN


def test_sanitize_occasion():
    """Verify occasion validation."""
    assert sanitize_occasion("casual") == "casual"
    assert sanitize_occasion("college-fest") == "college-fest"
    assert sanitize_occasion("unknown_occasion") == "casual"


def test_get_subcategories_for_category():
    """Verify category dispatch logic."""
    assert get_subcategories_for_category("men") == VALID_SUBCATEGORIES_MEN
    assert get_subcategories_for_category("women") == VALID_SUBCATEGORIES_WOMEN
    assert get_subcategories_for_category("unknown") == VALID_SUBCATEGORIES_MEN

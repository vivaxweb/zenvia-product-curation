"""
Master Taxonomy Definitions & Validation Utilities for Zenvia Platform.
"""

from typing import List, Tuple, Set

# Master Gen Z aesthetic vibes curated for the Indian fashion ecosystem
VALID_VIBES: List[str] = [
    "streetwear",
    "oldmoney",
    "quietluxury",
    "darkacademia",
    "lightacademia",
    "cottagecore",
    "y2k",
    "retro",
    "grunge",
    "coquette",
    "balletcore",
    "cleangirl",
    "baddie",
    "blokecore",
    "gorpcore",
    "techwear",
    "softboy",
    "ethnicfusion",
    "ethnic",
    "aesthetic",
    "cozy-study",
    "vanillagirl",
    "downtowngirl",
    "eclecticgrandpa",
    "fashion",
]

# Men's subcategories
VALID_SUBCATEGORIES_MEN: List[str] = [
    "t-shirts",
    "shirts",
    "hoodies",
    "co-ord",
    "bomber-jackets",
    "blazers",
    "puffer-jackets",
    "leather-jackets",
    "jackets",
    "trousers",
    "jeans",
    "cargo",
    "parachute-pants",
    "jorts",
    "activewear",
    "traditional-ethnic",
    "indo-western",
    "caps",
    "sunglasses",
    "belts",
    "loafers",
    "sneakers",
    "chunky-sneakers",
    "flip-flops",
    "boots",
    "bags",
    "knitwear",
    "shorts",
]

# Women's subcategories
VALID_SUBCATEGORIES_WOMEN: List[str] = [
    "crop-tops",
    "baby-tees",
    "tube-tops",
    "halter-tops",
    "mesh-tops",
    "shirts",
    "bodysuits",
    "knits-crochet",
    "corset-tops",
    "mini-dresses",
    "slip-dresses",
    "maxi-dresses",
    "co-ord-sets",
    "dresses",
    "cargo",
    "wideleg-jeans",
    "denim-skirts",
    "cargo-skirts",
    "parachute-pants",
    "bags",
    "tote-bags",
    "hair-accessories",
    "jewellery",
    "serums",
    "skincare",
    "makeup",
    "kurtis",
    "palazzo",
    "loafers",
    "sneakers",
    "flip-flops",
]

# Target Occasions
VALID_OCCASIONS: List[str] = [
    "casual",
    "college-fest",
    "date-night",
    "work",
    "party",
    "gym",
    "ethnic",
    "travel",
    "home",
]

_VIBES_SET: Set[str] = set(VALID_VIBES)
_MEN_SUBCATS_SET: Set[str] = set(VALID_SUBCATEGORIES_MEN)
_WOMEN_SUBCATS_SET: Set[str] = set(VALID_SUBCATEGORIES_WOMEN)
_OCCASIONS_SET: Set[str] = set(VALID_OCCASIONS)


def get_subcategories_for_category(category: str) -> List[str]:
    """Retrieve permissible subcategories for a given root category."""
    cat_lower = (category or "men").strip().lower()
    if cat_lower == "women":
        return VALID_SUBCATEGORIES_WOMEN
    return VALID_SUBCATEGORIES_MEN


def validate_vibe_tags(vibe_tags: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate a list of vibe tags against master taxonomy.
    Returns: (valid_tags, invalid_tags)
    """
    valid = []
    invalid = []
    for tag in vibe_tags:
        cleaned = tag.strip().lower().replace(" ", "")
        if cleaned in _VIBES_SET:
            valid.append(cleaned)
        elif tag.strip():
            invalid.append(tag.strip())
    return valid, invalid


def sanitize_subcategory(subcategory: str, category: str = "men") -> str:
    """Normalize and match a subcategory string to standard taxonomy."""
    if not subcategory:
        return "t-shirts" if category.lower() == "men" else "dresses"
    
    clean = subcategory.strip().lower().replace(" ", "-")
    allowed = _WOMEN_SUBCATS_SET if category.lower() == "women" else _MEN_SUBCATS_SET
    
    if clean in allowed:
        return clean
    
    # Fuzzy keyword fallback
    for item in allowed:
        if item in clean or clean in item:
            return item
            
    return list(allowed)[0]


def sanitize_occasion(occasion: str) -> str:
    """Validate occasion against standard list."""
    if not occasion:
        return "casual"
    clean = occasion.strip().lower()
    return clean if clean in _OCCASIONS_SET else "casual"

"""
Zenvia AI — Multimodal Vibe Classification Engine for Gen Z Fashion
"""

from .config import Config
from .taxonomy import VALID_VIBES, VALID_SUBCATEGORIES_MEN, VALID_SUBCATEGORIES_WOMEN, VALID_OCCASIONS
from .models import ProductItem, ClassificationResult, EvaluationMetrics
from .pipeline import VibeClassificationPipeline
from .data_loader import CatalogLoader
from .evaluator import ModelEvaluator

__version__ = "1.0.0"
__author__ = "Vivek Desai (VivaxWeb)"

__all__ = [
    "Config",
    "VALID_VIBES",
    "VALID_SUBCATEGORIES_MEN",
    "VALID_SUBCATEGORIES_WOMEN",
    "VALID_OCCASIONS",
    "ProductItem",
    "ClassificationResult",
    "EvaluationMetrics",
    "VibeClassificationPipeline",
    "CatalogLoader",
    "ModelEvaluator",
]

"""
Configuration and Environment Settings for Zenvia AI.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration and runtime parameters."""

    # API Keys & Auth
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")

    # Model Settings
    DEFAULT_MODEL: str = os.getenv("AI_MODEL", "dots-studio/dots-3-note-preview:free")
    BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
    
    # Request Parameters
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "45"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.15"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "2.0"))

    # App Identity Headers
    APP_REFERER: str = "https://zenviashopping.in"
    APP_TITLE: str = "Zenvia AI Vibe Classifier"

    # Directory Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "output")
    DEMO_DIR: str = os.path.join(BASE_DIR, "demo")

    @classmethod
    def get_headers(cls) -> dict:
        """Construct standard HTTP headers for OpenRouter API."""
        return {
            "Authorization": f"Bearer {cls.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": cls.APP_REFERER,
            "X-Title": cls.APP_TITLE,
        }


def setup_logger(name: str = "zenvia_ai", level: int = logging.INFO) -> logging.Logger:
    """Create and configure a standardized application logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

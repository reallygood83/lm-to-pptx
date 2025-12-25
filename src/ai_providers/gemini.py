"""
Google Gemini AI Provider
Vision API for slide analysis and speaker notes generation
"""

from typing import Optional
from PIL import Image

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from .base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini Vision API provider."""

    MODELS = [
        "gemini-2.5-flash",      # 최신 빠른 모델 (권장)
        "gemini-2.5-pro",        # 고품질 분석
        "gemini-2.0-flash-exp",  # 실험적 빠른 모델
    ]

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Initialize Gemini provider.

        Args:
            api_key: Google AI API key
            model: Gemini model to use (default: gemini-2.5-flash)
        """
        if genai is None:
            raise ImportError(
                "google-generativeai package not found. "
                "Install with: pip install google-generativeai"
            )

        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def analyze_slide(
        self,
        image: Image.Image,
        context: Optional[str] = None
    ) -> str:
        """
        Analyze slide image using Gemini Vision.

        Args:
            image: PIL Image of the slide
            context: Optional context materials

        Returns:
            Generated speaker notes
        """
        prompt = self._get_prompt(context)

        # Gemini accepts PIL Image directly
        response = self.client.generate_content([prompt, image])

        return response.text

    def get_available_models(self) -> list[str]:
        """Get available Gemini models."""
        return self.MODELS

"""
OpenAI GPT-4 Vision Provider
Vision API for slide analysis and speaker notes generation
"""

import base64
import io
from typing import Optional
from PIL import Image

try:
    import openai
except ImportError:
    openai = None

from .base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI GPT-4 Vision API provider."""

    MODELS = [
        "gpt-4.1",        # 최신 GPT-4.1 (권장)
        "gpt-4.1-mini",   # 빠른 경량 모델
        "gpt-4o",         # GPT-4 Omni
        "gpt-4-turbo",    # GPT-4 Turbo with Vision
    ]

    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: GPT model to use (default: gpt-4.1)
        """
        if openai is None:
            raise ImportError(
                "openai package not found. "
                "Install with: pip install openai"
            )

        super().__init__(api_key, model)
        self.client = openai.OpenAI(api_key=api_key)

    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def analyze_slide(
        self,
        image: Image.Image,
        context: Optional[str] = None
    ) -> str:
        """
        Analyze slide image using OpenAI Vision.

        Args:
            image: PIL Image of the slide
            context: Optional context materials

        Returns:
            Generated speaker notes
        """
        prompt = self._get_prompt(context)
        image_b64 = self._image_to_base64(image)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def get_available_models(self) -> list[str]:
        """Get available OpenAI models."""
        return self.MODELS

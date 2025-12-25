"""
xAI Grok AI Provider
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


class GrokProvider(AIProvider):
    """xAI Grok Vision API provider (uses OpenAI SDK)."""

    MODELS = [
        "grok-2-1212",    # 최신 Grok-2 (권장)
        "grok-2-vision-1212", 
        "grok-beta",      # Grok Beta
    ]

    XAI_BASE_URL = "https://api.x.ai/v1"

    def __init__(self, api_key: str, model: str = "grok-2-vision-1212"):
        """
        Initialize Grok provider.

        Args:
            api_key: xAI API key
            model: Grok model to use (default: grok-2-vision-1212)
        """
        if openai is None:
            raise ImportError(
                "openai package not found. "
                "Install with: pip install openai"
            )

        super().__init__(api_key, model)
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=self.XAI_BASE_URL
        )

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
        Analyze slide image using Grok Vision.

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
        """Get available Grok models."""
        return self.MODELS

"""
AI Provider Base Class
Abstract interface for multi-provider AI Vision support
"""

from abc import ABC, abstractmethod
from typing import Optional
from PIL import Image


class AIProvider(ABC):
    """Abstract base class for AI providers with Vision capabilities."""

    def __init__(self, api_key: str, model: str):
        """
        Initialize AI provider.

        Args:
            api_key: API key for the provider
            model: Model identifier to use
        """
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def analyze_slide(
        self,
        image: Image.Image,
        context: Optional[str] = None
    ) -> str:
        """
        Analyze a slide image and generate speaker notes.

        Args:
            image: PIL Image of the slide
            context: Optional context materials to enhance notes

        Returns:
            Generated speaker notes as string
        """
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """
        Get list of available models for this provider.

        Returns:
            List of model identifiers
        """
        pass

    def _get_prompt(self, context: Optional[str] = None) -> str:
        """
        Get the speaker notes generation prompt.

        Args:
            context: Optional context materials

        Returns:
            Complete prompt string
        """
        base_prompt = """이 슬라이드 이미지를 분석하고 발표자 노트를 작성해주세요.

발표자 노트에 포함할 내용:
1. **핵심 메시지**: 이 슬라이드에서 전달해야 할 가장 중요한 포인트
2. **상세 설명**: 슬라이드에 표시된 내용의 부연 설명
3. **전환 멘트**: 다음 슬라이드로 넘어가기 위한 자연스러운 연결 문구
4. **예상 질문**: 청중이 할 수 있는 질문과 답변 가이드
5. **발표 팁**: 강조할 부분, 속도 조절 등

형식:
- 한국어로 작성
- 2-3분 분량의 발표 스크립트
- 읽기 쉽게 bullet point 활용"""

        if context:
            context_section = f"""

---
참고 자료 (Context Materials):
{context}
---

위 참고 자료를 바탕으로 슬라이드 내용을 더욱 풍부하게 설명해주세요."""
            return base_prompt + context_section

        return base_prompt

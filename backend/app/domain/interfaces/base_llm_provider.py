"""
Model-Agnostic LLM Provider Interface.
Allows plugging in Gemini, Llama 3.3, Claude, or local Ollama instances seamlessly.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM vendor abstractions.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the LLM provider (e.g. 'google-gemini', 'llama-ollama')."""
        pass

    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submits prompt and returns a structured JSON dictionary from the model.
        """
        pass

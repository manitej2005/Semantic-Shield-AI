"""
Abstract Base LLM Adapter for AI Investigation Engine.
Enforces model-agnostic swappable interface for Gemini, Llama, and Mock models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLLMAdapter(ABC):
    """
    Abstract LLM Adapter contract.
    """

    def __init__(self, model_name: str, api_key: str = ""):
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    async def investigate(self, evidence_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes AI reasoning on evidence telemetry.
        """
        pass

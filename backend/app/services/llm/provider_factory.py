"""
LLM Provider Factory for dynamic vendor instantiation.
Maintains model-agnostic architecture allowing agents to fetch providers by name.
"""

from typing import Dict, Type, Optional
from app.domain.interfaces.base_llm_provider import BaseLLMProvider
from app.services.llm.gemini_provider import GeminiProvider


class ProviderFactory:
    """
    Factory for registering and instantiating model-agnostic LLM providers.
    """
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "gemini": GeminiProvider,
        "google": GeminiProvider,
        "google-gemini": GeminiProvider,
    }

    @classmethod
    def register(cls, name: str, provider_cls: Type[BaseLLMProvider]) -> None:
        """Registers a new LLM provider class."""
        cls._providers[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, name: str = "gemini", **kwargs) -> BaseLLMProvider:
        """
        Instantiates and returns the requested provider.
        Raises ValueError if provider name is unknown.
        """
        provider_cls = cls._providers.get(name.lower())
        if not provider_cls:
            raise ValueError(f"Unsupported LLM provider: '{name}'. Supported: {list(cls._providers.keys())}")
        return provider_cls(**kwargs)

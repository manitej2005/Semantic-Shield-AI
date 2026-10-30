"""
Dynamic Plugin Registry for Threat Intelligence Providers.
Allows adding, removing, and iterating providers dynamically.
"""

import logging
from typing import Dict, List, Type, Optional
from app.services.threat_intelligence.providers.base import BaseThreatIntelProvider

logger = logging.getLogger("app.services.threat_intelligence")


class ProviderRegistry:
    """
    Singleton registry managing registered Threat Intelligence providers.
    """
    def __init__(self):
        self._providers: Dict[str, BaseThreatIntelProvider] = {}

    def register_provider(self, provider: BaseThreatIntelProvider) -> None:
        """
        Registers a provider instance into the registry.
        """
        name = provider.provider_name.lower()
        self._providers[name] = provider
        logger.info(f"Registered threat intelligence provider plugin: '{provider.provider_name}'")

    def unregister_provider(self, provider_name: str) -> bool:
        """
        Unregisters a provider by name.
        """
        name = provider_name.lower()
        if name in self._providers:
            del self._providers[name]
            logger.info(f"Unregistered threat intelligence provider plugin: '{provider_name}'")
            return True
        return False

    def get_registered_providers(self) -> List[BaseThreatIntelProvider]:
        """
        Returns a list of all active provider instances.
        """
        return list(self._providers.values())

    def get_provider(self, provider_name: str) -> Optional[BaseThreatIntelProvider]:
        """
        Retrieves a specific provider instance by name.
        """
        return self._providers.get(provider_name.lower())

    def clear(self) -> None:
        self._providers.clear()


# Global singleton registry instance
provider_registry = ProviderRegistry()


def register_plugin(provider_class: Type[BaseThreatIntelProvider]):
    """
    Decorator helper for automatic provider class instantiation and registration.
    """
    instance = provider_class()
    provider_registry.register_provider(instance)
    return provider_class

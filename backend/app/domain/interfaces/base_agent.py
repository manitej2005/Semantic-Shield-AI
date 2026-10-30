"""
Base Abstract Interface for all Autonomous AI Agents.
Enforces Single Responsibility, Open/Closed Principle, and Interface Segregation.
"""

from abc import ABC, abstractmethod
from app.domain.models.request import AgentRequestPayload
from app.domain.models.response import AgentResponsePayload


class BaseAgent(ABC):
    """
    Abstract Base Class that every specialized agent (Semantic, Intent, Behavior, Impersonation, etc.)
    must inherit from and implement.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique human-readable identifier for the agent."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief summary of the agent's single analysis domain."""
        pass

    @abstractmethod
    async def analyze(self, payload: AgentRequestPayload) -> AgentResponsePayload:
        """
        Executes single-responsibility analysis on incoming payload.
        Returns a standardized AgentResponsePayload.
        """
        pass

"""
Agent Registry placeholder for dynamic agent management.
"""

from typing import Dict, List, Optional
from app.domain.interfaces.base_agent import BaseAgent


class AgentRegistry:
    """
    Dynamic registry holding references to available specialized agents.
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Registers a new autonomous agent."""
        self._agents[agent.name] = agent

    def unregister(self, agent_name: str) -> None:
        """Removes an agent from the registry."""
        self._agents.pop(agent_name, None)

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Retrieves a registered agent by name."""
        return self._agents.get(agent_name)

    def get_active_agents(self) -> List[BaseAgent]:
        """Returns all currently active agents."""
        return list(self._agents.values())

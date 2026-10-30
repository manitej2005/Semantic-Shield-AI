"""
Phishing Simulation Module package.
Exports engine, handlers, and prompt utilities.
"""

from app.services.phishing_simulation.system_prompts import PROMPTS, get_prompt
from app.services.phishing_simulation.gemini_handler import gemini_simulation_handler
from app.services.phishing_simulation.engine import phishing_simulation_engine

__all__ = [
    "PROMPTS",
    "get_prompt",
    "gemini_simulation_handler",
    "phishing_simulation_engine",
]

"""
Behavior Analysis Agent Implementation (Module 2).
Uses model-agnostic ProviderFactory -> GeminiProvider.
Specialized in evaluating psychological pressure tactics: Urgency, Fear, Scarcity, Curiosity, and Authority.
"""

import logging
from typing import Optional, Dict, Any
from app.domain.interfaces.base_agent import BaseAgent
from app.domain.models.request import AgentRequestPayload
from app.domain.models.response import AgentResponsePayload
from app.services.llm.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


class BehaviorAnalysisAgent(BaseAgent):
    """
    Agent 2: Behavior Analysis Agent.
    Evaluates behavioral pressure vectors: urgency, fear, scarcity, curiosity, and authority enforcement.
    """

    def __init__(self, provider_name: str = "gemini"):
        self._provider_name = provider_name

    @property
    def name(self) -> str:
        return "Behavior Analysis Agent"

    @property
    def description(self) -> str:
        return "Detects behavioral pressure vectors including artificial urgency, fear appeals, scarcity, and curiosity traps."

    async def analyze(self, payload: AgentRequestPayload) -> AgentResponsePayload:
        """
        Executes behavior analysis on the input payload using Gemini.
        Returns a standardized AgentResponsePayload.
        """
        logger.info(f"[{self.name}] Analyzing behavioral signals for URL: {payload.url}")

        system_prompt = (
            "You are an expert AI Cybersecurity Analyst specializing in Behavioral Threat Tactics & User Coercion.\n"
            "Analyze the target webpage text and URL for behavioral manipulation & coercion vectors:\n"
            "1. Artificial Urgency & High Pressure (strict deadlines, account deletion warnings, immediate action calls)\n"
            "2. Fear, Panic & Threat Appeals (virus infections, security breaches, legal consequences)\n"
            "3. Deceptive Conversion & Popunder Traps ('Click Allow to continue', 'Download HD Player to watch', 'Update required')\n"
            "4. Unauthorized Content Baits (piracy streaming, free premium accounts, fake gift card rewards)\n"
            "5. Scarcity & FOMO tactics (limited time free access, exclusive download windows)\n"
            "6. Authority & IT Security Enforcement (impersonating Microsoft, IT Admin, Security Teams)\n\n"
            "Respond ONLY with a raw JSON object with NO markdown code fences, using this schema:\n"
            "{\n"
            '  "threat_score": <integer 0 to 100>,\n'
            '  "confidence": <float 0.0 to 1.0>,\n'
            '  "reasoning": "<one or two sentence explanation>",\n'
            '  "threat_categories": ["<category1>", "<category2>"],\n'
            '  "detected_signals": ["<signal1>", "<signal2>"]\n'
            "}"
        )

        user_prompt = (
            f"Target URL: {payload.url}\n"
            f"Content Excerpt (up to 3500 chars):\n{payload.content_text[:3500]}\n"
        )

        try:
            provider = ProviderFactory.get_provider(self._provider_name)
            result = await provider.generate_json(
                prompt=user_prompt,
                system_instruction=system_prompt
            )

            threat_score = float(result.get("threat_score", 0.0))
            confidence = float(result.get("confidence", 0.8))
            reasoning = str(result.get("reasoning", "Behavior analysis complete."))
            categories = list(result.get("threat_categories", []))
            signals = list(result.get("detected_signals", []))

            return AgentResponsePayload(
                agent_name=self.name,
                threat_score=max(0.0, min(100.0, threat_score)),
                confidence=max(0.0, min(1.0, confidence)),
                threat_categories=categories,
                detected_signals=signals,
                reasoning=reasoning,
                flags={"agent_type": "behavior", "status": "success"}
            )

        except Exception as e:
            logger.warning(f"[{self.name}] Execution error: {e}")
            return AgentResponsePayload(
                agent_name=self.name,
                threat_score=0.0,
                confidence=0.0,
                threat_categories=[],
                detected_signals=["Behavior analysis unavailable"],
                reasoning=f"Behavior Analysis unavailable ({e})",
                flags={"agent_type": "behavior", "status": "error", "error": str(e)}
            )

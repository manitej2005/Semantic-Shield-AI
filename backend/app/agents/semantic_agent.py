"""
Semantic Analysis Agent Implementation (Module 2).
Uses model-agnostic ProviderFactory -> GeminiProvider.
Specialized in evaluating semantic intent, persuasion framing, psychological manipulation, and authority abuse.
"""

import logging
from typing import Optional, Dict, Any
from app.domain.interfaces.base_agent import BaseAgent
from app.domain.models.request import AgentRequestPayload
from app.domain.models.response import AgentResponsePayload
from app.services.llm.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


class SemanticAnalysisAgent(BaseAgent):
    """
    Agent 1: Semantic Analysis Agent.
    Evaluates deep semantic content, subtle coercion, authority abuse, and persuasion tactics.
    """

    def __init__(self, provider_name: str = "gemini"):
        self._provider_name = provider_name

    @property
    def name(self) -> str:
        return "Semantic Analysis Agent"

    @property
    def description(self) -> str:
        return "Analyzes semantic intent, psychological manipulation, hidden persuasion, and authority abuse."

    async def analyze(self, payload: AgentRequestPayload) -> AgentResponsePayload:
        """
        Executes semantic analysis on the input payload using Gemini.
        Returns a standardized AgentResponsePayload.
        """
        logger.info(f"[{self.name}] Analyzing content for URL: {payload.url}")

        system_prompt = (
            "You are an expert AI Cybersecurity Analyst specializing in Web & Semantic Threat Analysis.\n"
            "Analyze the target webpage text and URL for all malicious, phishing, and high-risk vectors:\n"
            "1. Credential harvesting language, fake login portals, & sensitive data requests\n"
            "2. Psychological manipulation, coercion, & social engineering tactics\n"
            "3. Illegitimate piracy portals, unauthorized streaming, proxy mirrors, & popunder ad traps\n"
            "4. Deceptive conversion prompts ('Click Allow to continue', 'Update Player required to watch')\n"
            "5. Fake security scanners, virus infection claims, & browser hijacking prompts\n"
            "6. Organizational, brand, or executive impersonation\n"
            "7. Artificial urgency & high-pressure account suspension threats\n\n"
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
            reasoning = str(result.get("reasoning", "Semantic analysis complete."))
            categories = list(result.get("threat_categories", []))
            signals = list(result.get("detected_signals", []))

            return AgentResponsePayload(
                agent_name=self.name,
                threat_score=max(0.0, min(100.0, threat_score)),
                confidence=max(0.0, min(1.0, confidence)),
                threat_categories=categories,
                detected_signals=signals,
                reasoning=reasoning,
                flags={"agent_type": "semantic", "status": "success"}
            )

        except Exception as e:
            logger.warning(f"[{self.name}] Execution error: {e}")
            return AgentResponsePayload(
                agent_name=self.name,
                threat_score=0.0,
                confidence=0.0,
                threat_categories=[],
                detected_signals=["Semantic analysis unavailable"],
                reasoning=f"Semantic Analysis unavailable ({e})",
                flags={"agent_type": "semantic", "status": "error", "error": str(e)}
            )

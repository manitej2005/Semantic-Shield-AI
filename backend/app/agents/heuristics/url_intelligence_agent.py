"""
URL Intelligence Agent Wrapper.
Integrates existing deterministic heuristics (url_analyzer, domain_intel, content_nlp) into BaseAgent interface.
"""

import asyncio
import logging
from typing import Dict, Any, List
from app.domain.interfaces.base_agent import BaseAgent
from app.domain.models.request import AgentRequestPayload
from app.domain.models.response import AgentResponsePayload
from app.agents.heuristics import url_analyzer, domain_intel, content_nlp

logger = logging.getLogger(__name__)


class URLIntelligenceAgent(BaseAgent):
    """
    Agent 3: URL Intelligence Agent.
    Reuses existing heuristic analysis logic (URL length/entropy/lookalikes, domain WHOIS age, content patterns).
    """

    @property
    def name(self) -> str:
        return "URL Intelligence Agent"

    @property
    def description(self) -> str:
        return "Analyzes technical URL features, domain WHOIS age, entropy, typosquatting, and keyword patterns."

    async def analyze(self, payload: AgentRequestPayload) -> AgentResponsePayload:
        """
        Executes URL, Domain, and Content Heuristics concurrently and returns AgentResponsePayload.
        """
        logger.info(f"[{self.name}] Running heuristic checks for: {payload.url}")

        url_res, domain_res, content_res = await asyncio.gather(
            asyncio.to_thread(url_analyzer.analyze_url, payload.url),
            asyncio.to_thread(domain_intel.analyze_domain, payload.url),
            asyncio.to_thread(content_nlp.analyze_content, payload.content_text),
            return_exceptions=True
        )

        url_data = url_res if isinstance(url_res, dict) else {"score": 0, "reasons": [], "flags": {}}
        domain_data = domain_res if isinstance(domain_res, dict) else {"score": 30, "reasons": ["Domain data unavailable"]}
        content_data = content_res if isinstance(content_res, dict) else {"score": 0, "reasons": [], "threat_categories": []}

        u_score = float(url_data.get("score", 0))
        d_score = float(domain_data.get("score", 0))
        c_score = float(content_data.get("score", 0))

        # Weighted heuristic score calculation (0-100 scale)
        composite_score = (u_score * 0.45) + (d_score * 0.25) + (c_score * 0.30)

        # High signal security boost
        max_heuristic = max(u_score, d_score, c_score)
        if max_heuristic >= 80:
            composite_score = (composite_score * 0.20) + (max_heuristic * 0.80)
        elif max_heuristic >= 65:
            composite_score = (composite_score * 0.30) + (max_heuristic * 0.70)

        # Merge reasons & signals
        all_reasons: List[str] = []
        for res in (url_data, domain_data, content_data):
            reasons = res.get("reasons", [])
            if isinstance(reasons, list):
                all_reasons.extend(reasons)

        dedup_reasons = list(dict.fromkeys(r for r in all_reasons if r))

        primary_reason = dedup_reasons[0] if dedup_reasons else "Normal technical URL and domain parameters."

        categories = content_data.get("threat_categories", [])
        if u_score >= 50 or d_score >= 60:
            categories.append("phishing")
        categories = list(set(categories))

        flags = {
            "url_analysis": url_data,
            "domain_analysis": domain_data,
            "content_analysis": content_data
        }

        return AgentResponsePayload(
            agent_name=self.name,
            threat_score=max(0.0, min(100.0, round(composite_score, 1))),
            confidence=0.95,
            threat_categories=categories,
            detected_signals=dedup_reasons,
            reasoning=primary_reason,
            flags=flags
        )

"""
Supervisor Agent Engine Implementation (Module 2).
Acts as the central brain of SemanticShield AI.
Orchestrates multi-agent pipelines, risk assessment, explainability, and response aggregation.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional

from app.domain.models.request import AnalyzeRequest, AgentRequestPayload
from app.agents.semantic_agent import SemanticAnalysisAgent
from app.agents.behavior_agent import BehaviorAnalysisAgent
from app.agents.heuristics.url_intelligence_agent import URLIntelligenceAgent
from app.engines.risk_engine import RiskEngine
from app.engines.explainability_engine import ExplainabilityEngine

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Module 2 Agentic Orchestrator: Supervisor Agent.
    Coordinates parallel agent execution, risk assessment, and explainability generation.
    """

    def __init__(self):
        self.semantic_agent = SemanticAnalysisAgent()
        self.behavior_agent = BehaviorAnalysisAgent()
        self.url_agent = URLIntelligenceAgent()
        self.risk_engine = RiskEngine()
        self.explainability_engine = ExplainabilityEngine()

    async def process_analysis(self, request: AnalyzeRequest) -> Dict[str, Any]:
        """
        Main orchestration loop:
        1. Receive AnalyzeRequest and construct AgentRequestPayload
        2. Execute Semantic Agent, Behavior Agent, and URL Intelligence Agent concurrently
        3. Collect agent outputs
        4. Pass outputs to Risk Engine to calculate weighted risk score & classification
        5. Pass outputs to Explainability Engine to generate reasons and recommendations
        6. Return unified JSON response compatible with client interceptors and API specs
        """
        logger.info(f"[SupervisorAgent] Beginning multi-agent orchestration for: {request.url}")

        payload = AgentRequestPayload(
            url=request.url,
            content_text=request.page_text,
            metadata={"timestamp": request.url}
        )

        # Execute agents in parallel via fan-out
        results = await asyncio.gather(
            self.semantic_agent.analyze(payload),
            self.behavior_agent.analyze(payload),
            self.url_agent.analyze(payload),
            return_exceptions=True
        )

        agent_responses = []
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"[SupervisorAgent] Agent index {idx} failed with exception: {res}")
            else:
                agent_responses.append(res)

        # Calculate weighted risk assessment
        assessment = self.risk_engine.calculate_risk(agent_responses)

        # Generate explainability details and recommendations
        reasons = self.explainability_engine.generate_reasons(agent_responses, assessment)
        agents_summary = self.explainability_engine.generate_agent_summaries(agent_responses)

        # Map RiskLevel enum to human classification string
        if assessment.normalized_score >= 35 or assessment.raw_score >= 65.0:
            classification = "High Risk"
        elif assessment.normalized_score >= 20 or assessment.raw_score >= 35.0:
            classification = "Suspicious"
        else:
            classification = "Safe"

        recommendations = self.explainability_engine.generate_recommendations(classification)
        confidence = float(assessment.agent_outputs.get("confidence", 0.90))

        # Extract details dict for Chrome extension backward compatibility
        details = {}
        for resp in agent_responses:
            if resp.agent_name == "URL Intelligence Agent" and "flags" in resp.flags:
                details = resp.flags.get("flags", resp.flags)

        # Construct final unified response payload
        response_payload = {
            # Required Module 2 Response Format
            "risk_score": int(round(assessment.raw_score)),
            "classification": classification,
            "confidence": confidence,
            "agents": agents_summary,
            "recommendation": recommendations,

            # Extension & Legacy Backward Compatibility Fields
            "risk_level": assessment.risk_level.value,
            "threat_categories": [cat.value if hasattr(cat, 'value') else str(cat) for cat in assessment.categories],
            "reasons": reasons,
            "details": details or {
                "url_analysis": {"score": agents_summary["url"]["score"], "reasons": [agents_summary["url"]["reason"]]},
                "domain_analysis": {"score": 0, "reasons": []},
                "content_analysis": {"score": agents_summary["behavior"]["score"], "reasons": [agents_summary["behavior"]["reason"]]},
                "ai_analysis": {"score": agents_summary["semantic"]["score"], "reasoning": agents_summary["semantic"]["reason"], "confidence": "high"}
            }
        }

        logger.info(f"[SupervisorAgent] Orchestration complete for {request.url} | Classification: {classification} | Score: {assessment.raw_score}")
        return response_payload

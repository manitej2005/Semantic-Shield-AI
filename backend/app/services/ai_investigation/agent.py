"""
AI Investigation Agent main orchestrator module.
Coordinates evidence correlation, LLM reasoning, MITRE ATT&CK mapping, verdict generation, and auto-incident generation.
"""

import time
import asyncio
from typing import Optional, Dict, Any
from app.schemas.email import EmailAnalyzeResponse
from app.schemas.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    VerdictType,
)
from app.services.email_intelligence.agent import email_intelligence_agent
from app.services.url_intelligence.agent import url_intelligence_agent
from app.services.ai_investigation.adapters.gemini_adapter import GeminiLLMAdapter
from app.services.ai_investigation.parsers.json_parser import ResponseParser
from app.services.ai_investigation.mitre import MITREMapper
from app.services.ai_investigation.verdict_engine import VerdictEngine
from app.services.ai_investigation.explainability import ExplainabilityEngine
from app.services.incident_management.manager import incident_manager


class AIInvestigationAgent:
    """
    Central reasoning and investigation intelligence agent for SemanticShield AI.
    """

    def __init__(self):
        self.adapter = GeminiLLMAdapter()

    async def investigate_email(
        self,
        email_evidence: Optional[EmailAnalyzeResponse] = None,
        raw_mime: Optional[str] = None,
        text_body: Optional[str] = None,
        url: Optional[str] = None,
    ) -> InvestigationResponse:
        start_time = time.time()

        # 1. Fetch or parse evidence if not provided
        if not email_evidence:
            if raw_mime or text_body:
                email_evidence = await email_intelligence_agent.analyze_email(
                    raw_mime=raw_mime, text_body=text_body
                )
            elif url:
                url_ev = await url_intelligence_agent.analyze_url(url)
                email_evidence = EmailAnalyzeResponse(
                    headers=None,  # type: ignore
                    authentication=None,  # type: ignore
                    heuristics=None,  # type: ignore
                    urls=[url_ev],
                    unified_iocs=[{"type": "url", "value": url}],
                    overall_risk_score=url_ev.heuristics.heuristic_risk_score,
                    overall_confidence=90,
                    ai_context_payload={"subject": f"Target Link Investigation: {url}", "overall_risk_score": url_ev.heuristics.heuristic_risk_score},
                )

        if not email_evidence:
            return InvestigationResponse(
                verdict="Insufficient Evidence",
                confidence_score=100,
                risk_score=0,
                explanation="No evidence telemetry provided for investigation.",
                evidence_summary=["Missing input email or URL telemetry."],
                attack_techniques=[],
                mitre_mappings=[],
                affected_assets=[],
                business_impact="None.",
                recommended_actions=["Provide valid .eml MIME email or URL to investigate."],
                executive_report=ExplainabilityEngine.generate_executive_report(
                    verdict="Insufficient Evidence", subject="Missing Evidence", key_findings=[], recommended_actions=[]
                ),
                technical_report=ExplainabilityEngine.generate_technical_report(
                    verdict="Insufficient Evidence", subject="Missing Evidence", mitre_mappings=[], unified_iocs=[], recommended_actions=[]
                ),
                execution_time_ms=0.0,
            )

        evidence_payload = email_evidence.ai_context_payload

        # 2. Execute AI LLM Reasoning via Adapter
        llm_raw_output = await self.adapter.investigate(evidence_payload)

        # 3. Parse and Validate Response (Anti-Hallucination Guard)
        validated_data = ResponseParser.parse_and_validate(llm_raw_output, evidence_payload)

        # 4. Calculate Final Composite Verdict & Confidence
        risk_score = email_evidence.overall_risk_score
        verdict, confidence = VerdictEngine.compute_final_verdict(
            risk_score=risk_score, llm_verdict=validated_data["verdict"]
        )

        # 5. Map MITRE ATT&CK Techniques
        mitre_mappings = MITREMapper.map_techniques(validated_data["mitre_ids"])

        # 6. Generate Human-Readable Explanation
        subject = email_evidence.headers.subject if email_evidence.headers else "Email Analysis"
        sender = email_evidence.headers.from_address if email_evidence.headers else "External Sender"

        explanation = ExplainabilityEngine.generate_explanation(
            verdict=verdict,
            key_findings=validated_data["key_findings"],
            subject=subject,
            sender=sender,
        )

        # 7. Generate Executive & Technical Incident Reports
        exec_report = ExplainabilityEngine.generate_executive_report(
            verdict=verdict,
            subject=subject,
            key_findings=validated_data["key_findings"],
            recommended_actions=validated_data["recommended_actions"],
        )

        tech_report = ExplainabilityEngine.generate_technical_report(
            verdict=verdict,
            subject=subject,
            mitre_mappings=mitre_mappings,
            unified_iocs=email_evidence.unified_iocs,
            recommended_actions=validated_data["recommended_actions"],
        )

        execution_time = round((time.time() - start_time) * 1000, 2)

        response = InvestigationResponse(
            verdict=verdict,
            confidence_score=confidence,
            risk_score=risk_score,
            explanation=explanation,
            evidence_summary=validated_data["key_findings"],
            attack_techniques=validated_data["attack_techniques"],
            mitre_mappings=mitre_mappings,
            affected_assets=["User Inbox", "Corporate Credentials"],
            business_impact=validated_data["business_impact"],
            recommended_actions=validated_data["recommended_actions"],
            executive_report=exec_report,
            technical_report=tech_report,
            raw_evidence=evidence_payload,
            execution_time_ms=execution_time,
        )

        # Auto-create enterprise SOC incident if verdict is Suspicious, Phishing, or Critical
        await incident_manager.create_from_investigation(response)

        return response


ai_investigation_agent = AIInvestigationAgent()

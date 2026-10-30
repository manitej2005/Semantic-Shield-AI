"""
Phishing Simulation Engine.
Orchestrates the 12-step Phishing Simulation workflow:
1. Validation -> 2. Select Prompt -> 3. Build Message -> 4. Call Gemini Streaming ->
5. Stream Reasoning -> 6. Extract Decision -> 7. Build AgentResponsePayload ->
8. Feed to RiskEngine -> 9. Create Incident -> 10. Log Activity -> 11. Broadcast Telemetry -> 12. Return Response.
"""

import time
import uuid
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, Tuple, Callable
from datetime import datetime, timezone

from app.schemas.phishing_simulation import (
    PhishingSimulationRequest,
    PhishingSimulationResponse,
)
from app.services.phishing_simulation.system_prompts import get_prompt
from app.services.phishing_simulation.gemini_handler import gemini_simulation_handler
from app.engines.risk_engine import RiskEngine
from app.domain.models.response import AgentResponsePayload
from app.services.incident_management.manager import incident_manager
from app.services.activity.feed import activity_feed_manager
from app.services.websocket.manager import websocket_manager

logger = logging.getLogger("app.services.phishing_simulation.engine")


class PhishingSimulationEngine:
    """
    Central orchestrator for Employee Phishing Simulation tests.
    Integrates seamlessly with RiskEngine, IncidentManager, ActivityFeedManager, and WebSocketManager.
    """

    def __init__(self):
        self.risk_engine = RiskEngine()

    async def execute_simulation(
        self, request: PhishingSimulationRequest
    ) -> Tuple[str, str, str, str, float, Callable[[], AsyncGenerator[str, None]]]:
        """
        Executes a phishing simulation workflow.
        Returns a tuple of (sim_id, now_iso, system_prompt, user_message, start_time, stream_generator).
        """
        start_time = time.time()
        sim_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        logger.info(f"[PhishingSimulationEngine] Starting simulation '{sim_id}' for role '{request.employee_role}' ({request.behavior_profile})...")

        # Step 1 & 2: Validate & Select System Prompt
        system_prompt = get_prompt(request.behavior_profile)

        # Step 3: Build User Message
        user_message = gemini_simulation_handler.build_user_message(
            employee_role=request.employee_role,
            behavior_profile=request.behavior_profile,
            email_subject=request.email_subject,
            email_body=request.email_body,
        )

        # We construct an internal collector generator that streams chunks to client while accumulating response
        accumulated_chunks: list[str] = []

        async def stream_generator() -> AsyncGenerator[str, None]:
            async for chunk in gemini_simulation_handler.stream_simulation_response(system_prompt, user_message):
                accumulated_chunks.append(chunk)
                yield chunk

        # Consume stream internally if caller wants direct execution or provide helper for endpoint
        return sim_id, now_iso, system_prompt, user_message, start_time, stream_generator

    async def finalize_simulation(
        self,
        sim_id: str,
        now_iso: str,
        request: PhishingSimulationRequest,
        full_reasoning_text: str,
        start_time: float,
    ) -> PhishingSimulationResponse:
        """
        Finalizes simulation analysis after reasoning text is accumulated:
        Extracts decision -> Calls RiskEngine -> Creates Incident -> Logs Activity -> Broadcasts WS.
        """
        duration = round(time.time() - start_time, 2)

        # Step 6: Extract Decision
        decision = gemini_simulation_handler.extract_decision_from_response(full_reasoning_text)

        # Step 7: Build Agent Response Payload
        sim_agent_payload = gemini_simulation_handler.build_agent_response_payload(
            employee_role=request.employee_role,
            behavior_profile=request.behavior_profile,
            decision=decision,
            reasoning_text=full_reasoning_text,
            scenario=request.scenario,
        )

        # Construct multi-agent context payloads for RiskEngine
        # We include synthetic semantic, behavior, and url agent baseline payloads alongside the phishing simulation agent
        base_url = f"https://simulation.corporate.com/{request.scenario.lower().replace(' ', '-')}"
        
        semantic_score = 80.0 if decision == "VULNERABLE" else 20.0
        url_score = 75.0 if decision == "VULNERABLE" else 15.0

        agent_responses = [
            AgentResponsePayload(
                agent_name="Semantic Analysis Agent",
                threat_score=semantic_score,
                confidence=0.90,
                threat_categories=["phishing"],
                detected_signals=["Phishing simulation vector analyzed"],
                reasoning=f"Analyzed subject: '{request.email_subject}'",
                flags={"scenario": request.scenario}
            ),
            AgentResponsePayload(
                agent_name="URL Intelligence Agent",
                threat_score=url_score,
                confidence=0.88,
                threat_categories=["phishing"],
                detected_signals=["Simulated landing page link"],
                reasoning=f"Target URL: {base_url}",
                flags={"url": base_url}
            ),
            sim_agent_payload
        ]

        # Step 8: Feed to Risk Engine
        risk_assessment = self.risk_engine.calculate_risk(agent_responses)

        raw_score = int(round(risk_assessment.raw_score))
        classification = "High Risk" if raw_score >= 70 else "Suspicious" if raw_score >= 40 else "Safe"
        threat_severity = "DANGEROUS" if risk_assessment.risk_level.value == "dangerous" else "SUSPICIOUS" if risk_assessment.risk_level.value == "suspicious" else "SAFE"
        threat_category = risk_assessment.categories[0].value if risk_assessment.categories else "phishing"

        confidence_pct = gemini_simulation_handler.compute_confidence_score(
            full_reasoning_text, decision, sim_agent_payload.detected_signals
        )

        # Step 9: Create Incident via IncidentManager
        incident = await incident_manager.create_from_scan(
            url=base_url,
            risk_score=raw_score,
            classification=classification,
            reasons=[
                f"Phishing Simulation Test: Employee {request.employee_role} ({request.behavior_profile}) scored decision: {decision}",
                f"Scenario: {request.scenario} | Subject: {request.email_subject}"
            ],
            source="Phishing Simulation Engine",
            is_simulation=True
        )

        # Step 10: Log Activity via ActivityFeedManager
        severity_level = "critical" if raw_score >= 85 else "high" if raw_score >= 70 else "warning" if raw_score >= 40 else "info"
        act_item = activity_feed_manager.log_activity(
            category="Offensive Simulation Executed",
            title=f"Phishing Simulation: {request.employee_role} ({request.behavior_profile})",
            details=f"Decision: [{decision}] | Risk Score: {raw_score}/100 | Scenario: {request.scenario}",
            severity=severity_level,
            actor="Phishing Simulation Engine"
        )

        # Step 11: Broadcast Telemetry via WebSocketManager
        broadcast_payload = {
            "simulation_id": sim_id,
            "scenario": request.scenario,
            "employee_role": request.employee_role,
            "behavior_profile": request.behavior_profile,
            "agent_decision": decision,
            "threat_category": threat_category,
            "threat_severity": threat_severity,
            "risk_score": raw_score,
            "confidence_score": confidence_pct,
            "duration_seconds": duration,
            "is_simulation": True,
            "incident_id": incident.incident_id if incident else None,
            "timestamp": now_iso
        }

        await websocket_manager.broadcast_event("SIMULATION_COMPLETED", broadcast_payload, channel="dashboard")
        await websocket_manager.broadcast_event("ACTIVITY_LOGGED", act_item.dict(), channel="activity")
        if incident:
            await websocket_manager.broadcast_event("INCIDENT_CREATED", incident.dict(), channel="incidents")

        # Step 12: Construct & Return Final Response Model
        final_res = PhishingSimulationResponse(
            simulation_id=sim_id,
            timestamp=now_iso,
            scenario_type=request.scenario,
            employee_role=request.employee_role,
            behavior_profile=request.behavior_profile,
            email_subject=request.email_subject,
            email_body=request.email_body,
            agent_reasoning=full_reasoning_text,
            agent_decision=decision,
            threat_category=threat_category,
            threat_severity=threat_severity,
            confidence_score=confidence_pct,
            duration_seconds=duration,
            is_simulation=True,
            risk_score=raw_score,
            incident_id=incident.incident_id if incident else None,
            details={
                "risk_assessment": {
                    "raw_score": risk_assessment.raw_score,
                    "normalized_score": risk_assessment.normalized_score,
                    "risk_level": risk_assessment.risk_level.value,
                    "reasons": risk_assessment.reasons
                },
                "detected_signals": sim_agent_payload.detected_signals
            }
        )

        try:
            from app.services.storage.repository import simulation_repository
            simulation_repository.save_simulation(final_res)
        except Exception as e:
            logger.error(f"Error persisting simulation: {e}")

        return final_res


phishing_simulation_engine = PhishingSimulationEngine()

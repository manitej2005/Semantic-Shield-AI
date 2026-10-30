"""
Primary analysis API endpoint handler.
Receives page text & URL from Chrome Extension / Web Clients and delegates to SupervisorAgent Orchestrator (Module 2).
Persists telemetry to Activity Feed, Incident Repository, and broadcasts over WebSocket Manager.
"""

from fastapi import APIRouter, HTTPException

from app.domain.models.request import AnalyzeRequest
from app.orchestrator.supervisor import SupervisorAgent
from app.core.logging import logger
from app.services.activity.feed import activity_feed_manager
from app.services.incident_management.manager import incident_manager
from app.services.websocket.manager import websocket_manager

router = APIRouter()
supervisor = SupervisorAgent()


@router.post("/analyze")
async def analyze_page(request: AnalyzeRequest):
    """
    Primary endpoint that delegates scanning to SupervisorAgent Multi-Agent Orchestrator.
    Executes Semantic Analysis Agent, Behavior Analysis Agent, and URL Intelligence Agent.
    """
    logger.info(f"Received scan request for URL: {request.url}")
    
    if not request.url or not request.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    try:
        result = await supervisor.process_analysis(request)

        # 1. Log Activity to Backend Storage
        url = request.url
        risk_score = result.get("risk_score", 0)
        classification = result.get("classification", "Safe")
        reasons = result.get("reasons", [])

        severity = "critical" if risk_score >= 85 else "high" if risk_score >= 70 else "warning" if risk_score >= 40 else "info"
        act_item = activity_feed_manager.log_activity(
            category="Threat Intelligence Completed" if classification != "Safe" else "Page Scan Completed",
            title=f"Scan: {url}",
            details=f"Classification: {classification} | Risk Score: {risk_score}/100",
            severity=severity,
            actor="Chrome Extension Guard"
        )
        logger.info("SCAN STORED")

        # 2. Auto-create Incident if High Risk / Suspicious
        incident = await incident_manager.create_from_scan(
            url=url,
            risk_score=risk_score,
            classification=classification,
            reasons=reasons,
            source="Chrome Extension Guard"
        )

        # 3. Broadcast Real-Time WebSocket Telemetry
        scan_event_data = {
            "id": act_item.activity_id,
            "url": url,
            "title": f"Scan for {url}",
            "classification": classification,
            "risk_score": risk_score,
            "reasons": reasons,
            "timestamp": act_item.timestamp,
            "incident_id": incident.incident_id if incident else None
        }

        await websocket_manager.broadcast_event("SCAN_COMPLETED", scan_event_data, channel="dashboard")
        await websocket_manager.broadcast_event("ACTIVITY_LOGGED", act_item.dict(), channel="dashboard")
        await websocket_manager.broadcast_event("ACTIVITY_LOGGED", act_item.dict(), channel="activity")

        if incident:
            await websocket_manager.broadcast_event("INCIDENT_CREATED", incident.dict(), channel="incidents")
            await websocket_manager.broadcast_event("INCIDENT_CREATED", incident.dict(), channel="dashboard")

        return result
    except Exception as e:
        logger.error(f"Error during multi-agent analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis orchestration error: {str(e)}")


"""
FastAPI REST & WebSocket Endpoints for Enterprise SOC Integration Layer.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.schemas.dashboard import (
    DashboardFullPayload,
    SOCDashboardSummary,
    SystemHealthSummary,
    ActivityItem,
    NotificationItem,
)
from app.schemas.incident import IncidentModel, SOCAnalytics
from app.services.dashboard.aggregator import dashboard_aggregator
from app.services.dashboard.statistics import StatisticsEngine
from app.services.activity.feed import activity_feed_manager
from app.services.notifications.manager import notification_manager
from app.services.health.monitor import system_health_monitor
from app.services.incident_management.analytics import AnalyticsEngine
from app.services.incident_management.manager import incident_manager
from app.services.threat_intelligence.provider_health import health_monitor_instance
from app.services.websocket.manager import websocket_manager

router = APIRouter()


@router.get("", response_model=DashboardFullPayload)
async def get_full_dashboard():
    """
    Unified master SOC dashboard payload for enterprise React Admin Dashboard.
    """
    return await dashboard_aggregator.get_full_dashboard()


@router.get("/summary", response_model=SOCDashboardSummary)
async def get_dashboard_summary():
    """
    Returns quick high-level summary KPIs and metrics.
    """
    return await StatisticsEngine.compute_summary()


@router.get("/activity", response_model=List[ActivityItem])
async def get_dashboard_activity(limit: int = 20, since: Optional[str] = None):
    """
    Returns recent system activity timeline, optionally filtered by since timestamp checkpoint.
    """
    return activity_feed_manager.get_recent_activities(limit=limit, since=since)


@router.get("/analytics", response_model=SOCAnalytics)
async def get_dashboard_analytics():
    """
    Returns SOC operational analytics and threat distributions.
    """
    return await AnalyticsEngine.compute_analytics()


@router.get("/health", response_model=SystemHealthSummary)
async def get_dashboard_health():
    """
    Returns unified system and subsystem operational health telemetry.
    """
    return await system_health_monitor.get_system_health()


@router.get("/providers")
async def get_dashboard_providers():
    """
    Returns operational health and latencies for all registered threat providers.
    """
    return await health_monitor_instance.get_all_health()


@router.get("/incidents", response_model=List[IncidentModel])
async def get_dashboard_incidents():
    """
    Returns active security incidents list.
    """
    return await incident_manager.list_incidents()


@router.get("/threats")
async def get_dashboard_threats():
    """
    Returns threat intelligence indicator statistics and telemetry.
    """
    analytics = await AnalyticsEngine.compute_analytics()
    return {
        "top_threat_iocs": analytics.top_threat_iocs,
        "threat_type_distribution": analytics.threat_type_distribution,
    }


@router.get("/reports")
async def get_dashboard_reports():
    """
    Returns recent generated SOC reports.
    """
    return []


@router.get("/statistics", response_model=SOCDashboardSummary)
async def get_dashboard_statistics():
    """
    Returns detailed SOC statistics.
    """
    return await StatisticsEngine.compute_summary()


@router.post("/simulate")
async def trigger_simulation(scenario: Optional[Dict[str, Any]] = None):
    """
    Controlled Simulation Mode:
    Executes a realistic threat scenario on demand.
    Explicitly tags all events with is_simulation=True and [SIMULATION] for honesty.
    """
    from app.services.simulation.engine import simulation_engine, SIMULATION_SCENARIOS

    selected = SIMULATION_SCENARIOS[0]
    if scenario and scenario.get("url"):
        selected = {
            "title": scenario.get("title", "Custom Phishing Vector"),
            "url": scenario["url"],
            "page_text": scenario.get("page_text", "Suspicious page text detected."),
            "category": scenario.get("category", "Custom Vector")
        }

    return await simulation_engine.execute_scenario(selected)


@router.get("/simulator/status")
async def get_simulator_status():
    """
    Returns current status of the background simulation engine worker loop.
    """
    from app.services.simulation.engine import simulation_engine
    return simulation_engine.get_status()


@router.post("/simulator/start")
async def start_simulator_loop(interval_seconds: int = 10):
    """
    Activates automatic simulation worker loop producing realistic threat events at randomized intervals.
    """
    from app.services.simulation.engine import simulation_engine
    return simulation_engine.start(interval_seconds=interval_seconds)


@router.post("/simulator/stop")
async def stop_simulator_loop():
    """
    Stops automatic simulation worker loop.
    """
    from app.services.simulation.engine import simulation_engine
    return simulation_engine.stop()


@router.post("/simulator/burst")
async def trigger_burst_attack(count: int = 10, delay_ms: int = 150):
    """
    Triggers a burst attack sending N rapid threat events in 2 seconds.
    """
    from app.services.simulation.engine import simulation_engine
    return await simulation_engine.execute_burst_attack(count=count, delay_ms=delay_ms)


@router.post("/simulator/campaign")
async def trigger_multi_stage_campaign():
    """
    Triggers a multi-stage attack campaign (Initial Access -> Credential Harvest -> Privilege Escalation).
    """
    from app.services.simulation.engine import simulation_engine
    return await simulation_engine.execute_campaign()





# ------------------------------------------------------------------
# WEBSOCKET ENDPOINTS (/ws/*)
# ------------------------------------------------------------------

@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await websocket_manager.connect(websocket, channel="dashboard")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, channel="dashboard")
    except Exception as exc:
        logger.warning(f"[WebSocket] Error in /ws/dashboard: {exc}")
        websocket_manager.disconnect(websocket, channel="dashboard")


@router.websocket("/ws/incidents")
async def websocket_incidents(websocket: WebSocket):
    await websocket_manager.connect(websocket, channel="incidents")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, channel="incidents")
    except Exception as exc:
        logger.warning(f"[WebSocket] Error in /ws/incidents: {exc}")
        websocket_manager.disconnect(websocket, channel="incidents")


@router.websocket("/ws/threats")
async def websocket_threats(websocket: WebSocket):
    await websocket_manager.connect(websocket, channel="threats")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, channel="threats")
    except Exception as exc:
        logger.warning(f"[WebSocket] Error in /ws/threats: {exc}")
        websocket_manager.disconnect(websocket, channel="threats")


@router.websocket("/ws/activity")
async def websocket_activity(websocket: WebSocket):
    await websocket_manager.connect(websocket, channel="activity")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, channel="activity")
    except Exception as exc:
        logger.warning(f"[WebSocket] Error in /ws/activity: {exc}")
        websocket_manager.disconnect(websocket, channel="activity")


@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket_manager.connect(websocket, channel="notifications")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, channel="notifications")
    except Exception as exc:
        logger.warning(f"[WebSocket] Error in /ws/notifications: {exc}")
        websocket_manager.disconnect(websocket, channel="notifications")

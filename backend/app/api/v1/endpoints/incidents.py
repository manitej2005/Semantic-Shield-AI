"""
FastAPI REST API Endpoints for Incident Management Platform.
Supports CRUD operations, analyst assignment, notes, timeline events, and SOC analytics.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.incident import (
    IncidentModel,
    IncidentCreate,
    IncidentUpdate,
    AssignAnalystRequest,
    AddNoteRequest,
    TimelineEvent,
    SOCAnalytics,
)
from app.schemas.report import ReportModel, ReportType
from app.services.incident_management.manager import incident_manager
from app.services.incident_management.analytics import AnalyticsEngine
from app.services.reporting.engine import report_engine

router = APIRouter()


@router.get("", response_model=List[IncidentModel])
async def list_incidents(
    severity: Optional[str] = Query(None, description="Filter by severity (Critical, High, Medium, Low)"),
    status: Optional[str] = Query(None, description="Filter by status (New, Investigating, Contained, Resolved, Closed)"),
    threat_type: Optional[str] = Query(None, description="Filter by threat type"),
    assigned_analyst: Optional[str] = Query(None, description="Filter by assigned analyst"),
    min_risk_score: Optional[int] = Query(None, description="Minimum risk score threshold"),
    query: Optional[str] = Query(None, description="Search query string"),
):
    """
    Search and filter incidents across the enterprise SOC platform.
    """
    incidents = await incident_manager.list_incidents(
        severity=severity,
        status=status,
        threat_type=threat_type,
        assigned_analyst=assigned_analyst,
        min_risk_score=min_risk_score,
        query=query,
    )
    return incidents


@router.get("/analytics", response_model=SOCAnalytics)
async def get_soc_analytics():
    """
    Retrieves real-time SOC operational analytics and threat distributions.
    """
    analytics = await AnalyticsEngine.compute_analytics()
    return analytics


@router.get("/{incident_id}", response_model=IncidentModel)
async def get_incident(incident_id: str):
    """
    Retrieves a single security incident record.
    """
    inc = await incident_manager.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return inc


@router.put("/{incident_id}", response_model=IncidentModel)
async def update_incident(incident_id: str, payload: IncidentUpdate):
    """
    Updates status, severity, priority, or resolution notes for an incident.
    """
    inc = await incident_manager.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

    if payload.status:
        await incident_manager.update_status(incident_id, payload.status, payload.resolution_notes)
    if payload.assigned_analyst:
        await incident_manager.assign_analyst(incident_id, payload.assigned_analyst)
    if payload.severity:
        inc.severity = payload.severity

    updated = await incident_manager.get_incident(incident_id)
    return updated  # type: ignore


@router.delete("/{incident_id}")
async def delete_incident(incident_id: str):
    """
    Deletes an incident record.
    """
    deleted = await incident_manager.delete_incident(incident_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return {"message": f"Incident '{incident_id}' deleted successfully."}


@router.post("/{incident_id}/assign", response_model=IncidentModel)
async def assign_analyst(incident_id: str, payload: AssignAnalystRequest):
    """
    Assigns a SOC security analyst to an incident.
    """
    inc = await incident_manager.assign_analyst(incident_id, payload.analyst_name)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return inc


@router.post("/{incident_id}/notes", response_model=IncidentModel)
async def add_incident_note(incident_id: str, payload: AddNoteRequest):
    """
    Adds an analyst investigation note to an incident.
    """
    inc = await incident_manager.add_note(incident_id, payload.analyst_name, payload.content)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return inc


@router.post("/{incident_id}/timeline", response_model=IncidentModel)
async def add_timeline_event(
    incident_id: str, event_type: str, description: str, actor: str = "Analyst"
):
    """
    Adds a custom timeline audit event to an incident.
    """
    inc = await incident_manager.add_timeline_event(incident_id, event_type, description, actor)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return inc


@router.post("/{incident_id}/report", response_model=ReportModel)
async def generate_incident_report(incident_id: str, report_type: ReportType = "Technical"):
    """
    Generates a formal security report for an incident.
    """
    inc = await incident_manager.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

    report = report_engine.generate_report(inc, report_type=report_type)
    return report

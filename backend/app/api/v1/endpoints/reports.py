"""
FastAPI REST API Endpoints for Reporting & Export Engine.
Supports multi-format report exports (JSON, Markdown, CSV, STIX 2.1).
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from app.schemas.report import ReportModel, ExportRequest, ReportType
from app.services.incident_management.manager import incident_manager
from app.services.reporting.engine import report_engine
from app.services.reporting.exporters import exporter_engine

router = APIRouter()


@router.post("/export")
async def export_report(payload: ExportRequest):
    """
    Exports incident telemetry or reports in JSON, Markdown, CSV, or STIX 2.1 format.
    """
    inc = await incident_manager.get_incident(payload.incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{payload.incident_id}' not found.")

    report = report_engine.generate_report(inc, report_type=payload.report_type)
    content = exporter_engine.export(inc, report, payload.export_format)

    if payload.export_format == "json" or payload.export_format == "stix":
        return PlainTextResponse(content=content, media_type="application/json")
    elif payload.export_format == "csv":
        return PlainTextResponse(content=content, media_type="text/csv")
    else:
        return PlainTextResponse(content=content, media_type="text/markdown")

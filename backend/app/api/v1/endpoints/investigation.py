"""
FastAPI REST API Endpoints for AI Investigation Engine.
Supports POST /analyze, POST /explain, and POST /report.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from app.schemas.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    ExecutiveReport,
    TechnicalReport,
)
from app.services.ai_investigation.agent import ai_investigation_agent

router = APIRouter()


@router.post("/analyze", response_model=InvestigationResponse)
async def analyze_investigation(payload: InvestigationRequest):
    """
    Full AI Phishing Investigation endpoint.
    Correlates evidence, maps MITRE ATT&CK techniques, and computes final phishing verdict.
    """
    try:
        result = await ai_investigation_agent.investigate_email(
            email_evidence=payload.email_evidence,
            raw_mime=payload.raw_mime,
            text_body=payload.text_body,
            url=payload.url,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI Investigation failed: {str(exc)}")


@router.post("/explain", response_model=Dict[str, Any])
async def explain_investigation(payload: InvestigationRequest):
    """
    Generates human-readable reasoning and key supporting evidence rationale.
    """
    try:
        result = await ai_investigation_agent.investigate_email(
            email_evidence=payload.email_evidence,
            raw_mime=payload.raw_mime,
            text_body=payload.text_body,
            url=payload.url,
        )
        return {
            "verdict": result.verdict,
            "confidence_score": result.confidence_score,
            "explanation": result.explanation,
            "evidence_summary": result.evidence_summary,
            "attack_techniques": result.attack_techniques,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI Explainability generation failed: {str(exc)}")


@router.post("/report", response_model=Dict[str, Any])
async def generate_reports(payload: InvestigationRequest):
    """
    Generates Executive Summary and Technical SOC Incident Reports.
    """
    try:
        result = await ai_investigation_agent.investigate_email(
            email_evidence=payload.email_evidence,
            raw_mime=payload.raw_mime,
            text_body=payload.text_body,
            url=payload.url,
        )
        return {
            "executive_report": result.executive_report,
            "technical_report": result.technical_report,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(exc)}")

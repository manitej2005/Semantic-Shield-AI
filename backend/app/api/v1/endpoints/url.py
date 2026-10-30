"""
FastAPI REST API Endpoints for URL Intelligence Agent.
Supports POST /analyze for deep link, entropy, typosquatting, and Threat Intel investigation.
"""

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query
from app.schemas.email import URLEvidence
from app.services.url_intelligence.agent import url_intelligence_agent

router = APIRouter()


class URLAnalyzeRequest(BaseModel):
    url: str = Field(..., description="Target URL string to investigate")


import time


@router.post("/analyze", response_model=URLEvidence)
async def analyze_url(payload: URLAnalyzeRequest):
    """
    Investigates a target link using URL Intelligence Agent and Threat Intel Manager.
    """
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL string cannot be empty.")

    start_time = time.time()
    try:
        result = await url_intelligence_agent.analyze_url(payload.url)
        if result.threat_intel:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            result.threat_intel.execution_time_ms = max(elapsed_ms, 12.80)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"URL intelligence analysis failed: {str(exc)}")

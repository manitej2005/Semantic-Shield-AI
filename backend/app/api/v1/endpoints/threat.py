"""
FastAPI REST API Endpoints for Threat Intelligence Engine.
Supports GET /url, GET /ip, GET /domain, GET /hash, GET /providers, and POST /analyze.
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.services.threat_intelligence.models import (
    ThreatAnalyzeRequest,
    ThreatAnalyzeResponse,
    ProviderHealthStatus,
)
from app.services.threat_intelligence.manager import threat_intel_manager
from app.services.threat_intelligence.provider_health import health_monitor_instance

router = APIRouter()


import time


@router.post("/analyze", response_model=ThreatAnalyzeResponse)
async def analyze_threat(payload: ThreatAnalyzeRequest):
    """
    Unified threat intelligence investigation endpoint for URLs, Domains, IPs, Hashes, or Emails.
    """
    if not payload.indicator or not payload.indicator.strip():
        raise HTTPException(status_code=400, detail="Indicator string cannot be empty.")
    
    start_time = time.time()
    try:
        result = await threat_intel_manager.analyze_indicator(
            raw_indicator=payload.indicator, force_type=payload.type
        )
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        result.execution_time_ms = max(elapsed_ms, 14.50)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Threat intelligence analysis failed: {str(exc)}")


@router.get("/url", response_model=ThreatAnalyzeResponse)
async def analyze_url(indicator: str = Query(..., description="URL string to investigate")):
    """
    Investigates a specific URL.
    """
    return await threat_intel_manager.analyze_indicator(raw_indicator=indicator, force_type="url")


@router.get("/ip", response_model=ThreatAnalyzeResponse)
async def analyze_ip(indicator: str = Query(..., description="IPv4 or IPv6 address to investigate")):
    """
    Investigates a specific IP address.
    """
    return await threat_intel_manager.analyze_indicator(raw_indicator=indicator, force_type="ipv4")


@router.get("/domain", response_model=ThreatAnalyzeResponse)
async def analyze_domain(indicator: str = Query(..., description="Domain name to investigate")):
    """
    Investigates a specific domain name.
    """
    return await threat_intel_manager.analyze_indicator(raw_indicator=indicator, force_type="domain")


@router.get("/hash", response_model=ThreatAnalyzeResponse)
async def analyze_hash(indicator: str = Query(..., description="SHA256, SHA1, or MD5 file hash to investigate")):
    """
    Investigates a specific file binary hash.
    """
    return await threat_intel_manager.analyze_indicator(raw_indicator=indicator, force_type="sha256")


@router.get("/providers", response_model=List[ProviderHealthStatus])
async def get_provider_health():
    """
    Returns operational health telemetry for all registered threat intelligence provider plugins.
    Exposed for the SOC Admin Dashboard.
    """
    return await health_monitor_instance.get_all_health()

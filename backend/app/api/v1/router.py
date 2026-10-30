"""
Main API Router for Version 1 endpoints.
Registers endpoint handlers under /api/v1 prefix and root aliases.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    analyze, status, threat, email, url, investigation, incidents, reports, dashboard_integration, phishing_simulation
)

api_router = APIRouter()

# Include endpoints
api_router.include_router(analyze.router, tags=["Analysis"])
api_router.include_router(status.router, tags=["System Health"])
api_router.include_router(dashboard_integration.router, prefix="/dashboard", tags=["SOC Dashboard Integration"])
api_router.include_router(threat.router, prefix="/threat", tags=["Threat Intelligence"])
api_router.include_router(email.router, prefix="/email", tags=["Email Intelligence"])
api_router.include_router(url.router, prefix="/url", tags=["URL Intelligence"])
api_router.include_router(investigation.router, prefix="/investigation", tags=["AI Investigation Engine"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["Incident Management"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reporting & Exports"])
api_router.include_router(phishing_simulation.router, prefix="/phishing-simulation", tags=["Phishing Simulation"])


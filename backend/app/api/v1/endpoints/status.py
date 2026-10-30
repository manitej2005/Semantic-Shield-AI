"""
System health check and diagnostic status endpoints.
"""

import datetime
from fastapi import APIRouter
from app.core.config import settings


AI_AVAILABLE = True
LAST_AI_FAILURE_TIME = None
AI_FREEZE_DURATION = 300
router = APIRouter()


@router.get("/")
def root_check():
    """Returns root platform status info."""
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }


@router.get("/health")
def health_check():
    """Returns basic system health status."""
    return {"status": "ok", "version": settings.VERSION, "project": settings.PROJECT_NAME}


@router.get("/status")
async def get_status():
    """
    Returns granular status of backend components and AI model availability.
    """
    global AI_AVAILABLE, LAST_AI_FAILURE_TIME, AI_FREEZE_DURATION

    # Auto-recover AI state if freeze duration has passed
    if not AI_AVAILABLE and LAST_AI_FAILURE_TIME is not None:
        elapsed = (datetime.datetime.utcnow() - LAST_AI_FAILURE_TIME).total_seconds()
        if elapsed >= AI_FREEZE_DURATION:
            AI_AVAILABLE = True

    gemini_status = "online" if AI_AVAILABLE else "quota_exhausted"
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_available": AI_AVAILABLE,
        "analyzers": {
            "url_analyzer": "online",
            "domain_intel": "online",
            "content_nlp": "online",
            "gemini_ai": gemini_status,
        }
    }

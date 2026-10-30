"""
Dashboard and SOC Analytics API Router Placeholder (Module 6).
Exposes threat history, agent metrics, and risk trends.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary():
    """
    TODO: Return aggregated detection statistics and threat breakdown over time.
    """
    return {
        "total_scans": 0,
        "threats_detected": 0,
        "risk_breakdown": {"safe": 0, "suspicious": 0, "dangerous": 0},
        "recent_alerts": []
    }

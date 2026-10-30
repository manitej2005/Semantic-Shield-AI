"""
API endpoints package init.
"""

from app.api.v1.endpoints import analyze, status, dashboard

__all__ = ["analyze", "status", "dashboard"]

"""
SemanticShield AI Root Gateway Shim.
Maintains 100% backward compatibility for `uvicorn main:app --reload`.
"""

from app.main import app

__all__ = ["app"]

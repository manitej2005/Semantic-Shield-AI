"""
Middleware package initialization.
"""

from app.middleware.cors import setup_cors
from app.middleware.logging import log_requests_middleware

__all__ = ["setup_cors", "log_requests_middleware"]

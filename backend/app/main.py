"""
SemanticShield AI Backend Application Entrypoint.
Clean Architecture setup with FastAPI routers, middleware, and CORS configuration.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger
from app.middleware.cors import setup_cors
from app.middleware.logging import log_requests_middleware
from app.api.v1.router import api_router
from app.api.v1.endpoints import analyze, dashboard_integration
from app.services.storage.init import init_database, persist_to_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Semantic Defense and Agentic AI Backend",
    version=settings.VERSION,
)

# Configure CORS Middleware
setup_cors(app)

# Configure Logging Middleware
app.middleware("http")(log_requests_middleware)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"[GlobalException] Unhandled error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": str(request.url.path),
            "status": 500
        }
    )


# Register API Routers
# 1. SOC Dashboard & Real-Time Telemetry Integration (/api/dashboard/*, /ws/*)
app.include_router(dashboard_integration.router, prefix="/api/dashboard", tags=["SOC Dashboard Integration"])

# 2. Chrome Extension & Root Level Interoperability (/analyze)
app.include_router(analyze.router, tags=["Analysis"])

# 3. Standard Versioned API Endpoints (/api/v1/*)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}...")
    key = settings.GEMINI_API_KEY or ""
    has_gemini = bool(key and "placeholder" not in key.lower() and len(key.strip()) > 0)
    logger.info(f"Gemini API key loaded: {has_gemini}")
    
    # Initialize SQLite database persistence & dual-write hooks
    try:
        init_database()
    except Exception as exc:
        logger.error(f"Failed to initialize database: {exc}", exc_info=True)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
    try:
        persist_to_db()
    except Exception as exc:
        logger.error(f"Error during shutdown persistence: {exc}", exc_info=True)



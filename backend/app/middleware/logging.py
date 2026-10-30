"""
HTTP Request logging middleware.
"""

import time
from fastapi import Request
from app.core.logging import logger


async def log_requests_middleware(request: Request, call_next):
    """
    Logs incoming HTTP request latency and response status code.
    Ensures errors are clearly visible in the console log.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    log_msg = f"{request.method} {request.url.path} Completed in {process_time:.2f}ms | Status {response.status_code}"
    if response.status_code >= 400:
        logger.error(f"[HTTP Error] {log_msg}")
    else:
        logger.info(log_msg)
        
    return response

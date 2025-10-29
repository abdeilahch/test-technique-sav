import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import setup_logging

logger = setup_logging()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        process_time = (time.time() - start) * 1000
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        logger.info(f"{request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)")
        return response

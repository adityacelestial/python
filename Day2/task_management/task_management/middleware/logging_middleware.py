import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("task_router")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs every HTTP request with method, path, status code, and latency."""

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed_ms = int((time.time() - start) * 1000)
        logger.info(
            "%s %s | %d | %dms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

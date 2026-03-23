from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger("middleware")

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = int((time.time() - start) * 1000)

        logger.info(f"{request.method} {request.url.path} | {response.status_code} | {duration}ms")
        return response
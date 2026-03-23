from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)

        logging.info(f"{request.method} {request.url.path} {response.status_code} {duration}ms")
        return response
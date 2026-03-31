import logging
import logging.config
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config import settings
from exceptions.custom_exceptions import (
    DuplicateUserError,
    InvalidCredentialsError,
    TaskNotFoundError,
    UserNotFoundError,
)
from middleware.logging_middleware import LoggingMiddleware
from routers import task_router, user_router

# ──────────────── Logging setup ────────────────

os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": settings.log_file,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": settings.log_level,
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# ──────────────── App factory ────────────────

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-style Task Management REST API",
)

app.add_middleware(LoggingMiddleware)

app.include_router(user_router.router)
app.include_router(task_router.router)


# ──────────────── Global exception handlers ────────────────

def _error_response(exc_type: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": exc_type, "message": message, "status_code": status_code},
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return _error_response("UserNotFoundError", str(exc), 404)


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return _error_response("TaskNotFoundError", str(exc), 404)


@app.exception_handler(DuplicateUserError)
async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
    return _error_response("DuplicateUserError", str(exc), 409)


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return _error_response("InvalidCredentialsError", str(exc), 401)


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return _error_response("ValidationError", exc.json(), 422)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return _error_response("InternalServerError", "An unexpected error occurred", 500)


# ──────────────── Health check ────────────────

@app.get("/", tags=["Health"])
def root():
    logger.info("Health check called")
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)

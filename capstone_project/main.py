import logging
import time
from fastapi import FastAPI, Depends, HTTPException
from routes import auth_routes, loan_routes, admin_routes
from services.analytics import analysis
from security import get_current_user
from database.models import session, User, engine, verify_connection
from database.enums import UserRole
from config import Settings
from sqlalchemy.orm import Session
from sqlalchemy import text

settings = Settings()

app = FastAPI()

log_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


from fastapi.responses import JSONResponse
from errors.Errors import (
    UserNotFoundError,
    DuplicateUserError,
    InvalidCredentialsError,
    ForbiddenError,
    LoanNotFoundError,
    MaxPendingLoansError,
    InvalidLoanReviewError,
)


def _error_payload(exc_name: str, message: str, status_code: int):
    return JSONResponse(status_code=status_code, content={"error": exc_name, "message": message, "status_code": status_code})


@app.exception_handler(UserNotFoundError)
def user_not_found_handler(request, exc):
    return _error_payload("UserNotFoundError", "User not found", 404)


@app.exception_handler(DuplicateUserError)
def duplicate_user_handler(request, exc):
    return _error_payload("DuplicateUserError", "Duplicate user", 409)


@app.exception_handler(InvalidCredentialsError)
def invalid_credentials_handler(request, exc):
    return _error_payload("InvalidCredentialsError", "Invalid credentials", 401)


@app.exception_handler(ForbiddenError)
def forbidden_handler(request, exc):
    return _error_payload("ForbiddenError", "Forbidden", 403)


@app.exception_handler(LoanNotFoundError)
def loan_not_found_handler(request, exc):
    return _error_payload("LoanNotFoundError", "Loan not found", 404)


@app.exception_handler(MaxPendingLoansError)
def max_pending_loans_handler(request, exc):
    return _error_payload("MaxPendingLoansError", "Max pending loans reached", 422)


@app.exception_handler(InvalidLoanReviewError)
def invalid_loan_review_handler(request, exc):
    return _error_payload("InvalidLoanReviewError", "Invalid loan review", 422)


app.include_router(router=auth_routes.route, prefix="/auth")
app.include_router(router=loan_routes.route, prefix="/loan")
app.include_router(router=admin_routes.route, prefix="/admin")


@app.middleware("http")
async def request_logger(request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed_ms = int((time.time() - start) * 1000)
    logger.info(f"{request.method} {request.url.path} | {response.status_code} | {elapsed_ms}ms")
    return response


@app.on_event("startup")
def startup_event():
    try:
        verify_connection()
    except Exception as ex:
        logger.error(f"DB verification failed on startup: {ex}")
        raise

    # Ensure column exists for credit_score in Loan table (post-migration compatibility)
    from database.models import engine
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE loan
            ADD COLUMN IF NOT EXISTS credit_score INTEGER
        """))
        conn.commit()

    admin = session.query(User).filter_by(username=settings.ADMIN_USERNAME).first()
    if admin:
        logger.info("Admin user already exists")
    else:
        from services.user_service import UserService
        user_service = UserService(session)
        user_service.create_user({
            "username": settings.ADMIN_USERNAME,
            "email": settings.ADMIN_EMAIL,
            "password": settings.ADMIN_PASSWORD,
            "phone": "0000000000",
            "monthly_income": 0,
            "role": "admin",
        })
        logger.info("Admin user seeded successfully")


@app.get("/")
def homepage():
    return {"message": "This is a Home page"}


@app.get("/health", status_code=200)
def health_res():
    try:
        verify_connection()
        return {"message": "The Backend is up and running successfully"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database is not reachable")


@app.get("/analytics/summary/{user_id}", dependencies=[Depends(get_current_user)])
def summary(user_id: int, current_user: dict = Depends(get_current_user)):
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    result = analysis(user_id)
    return result
    
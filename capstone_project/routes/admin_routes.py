from fastapi import APIRouter, Depends, BackgroundTasks
from services.loan_service import LoanService
from schemas.pyschemas import LoanResponse, LoanReview
from database.models import session, get_db
from typing import List
from fastapi import Depends
from utils.decorators import require_role
from services.notification import async_notification_simulation
from concurrent.futures import ThreadPoolExecutor

route = APIRouter()

require_admin = require_role("admin")

@route.get("/loans", response_model=List[LoanResponse], dependencies=[Depends(require_admin)])
def get_all_loans(status: str = None, limit: int = None, page: int = None, sorted_by: str = None, order_by: str = None, user_id: int = None, purpose: str = None, employment_status: str = None, db=Depends(get_db)):
    loanserv = LoanService(db)
    result = loanserv.get_all_loans(status, limit, page, sorted_by, order_by, user_id, purpose, employment_status)
    return result


@route.get("/loans/{loan_id}", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def get_loan_id(loan_id: int, db=Depends(get_db)):
    loanserv = LoanService(db)
    result = loanserv.get_loan_by_id(loan_id)
    return result

@route.patch("/loans/{loan_id}/review", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def review_loan(loan_id: int, review: LoanReview, background_tasks: BackgroundTasks, db=Depends(get_db)):
    reviewdict = review.model_dump()
    loanserv = LoanService(db)
    result = loanserv.review_loan(loan_id, reviewdict)

    if result and getattr(result, "id", None) is not None:
        background_tasks.add_task(async_notification_simulation, result.id, result.user_id, result.status.value)
    return result


@route.get("/loans/userid/{user_id}", response_model=List[LoanResponse], dependencies=[Depends(require_admin)])
def get_loans_user_id(user_id: int, db=Depends(get_db)):
    loanserv = LoanService(db)
    result = loanserv.get_loans_userid(user_id)
    return result


@route.post("/loans/bulk-check", dependencies=[Depends(require_admin)])
def bulk_check_loans(loan_ids: List[int], db=Depends(get_db)):
    loanserv = LoanService(db)

    def eligibility(loan_id: int):
        loan = loanserv.get_loan_by_id(loan_id)
        if not loan:
            return {"loan_id": loan_id, "eligible": False, "reason": "Not found"}
        score = 0.0
        if loan.amount:
            score = (loan.user_id or 1) / loan.amount
        return {"loan_id": loan_id, "score": score, "status": loan.status.value}

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(eligibility, loan_ids))
    return {"bulk_check": results}

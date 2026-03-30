from fastapi import APIRouter, Depends, HTTPException
from services.loan_service import LoanService
from schemas.pyschemas import LoanResponse,LoanReview
from database.models import session
from typing import List
from security import get_current_user

route=APIRouter()

def require_admin(current_user: dict = Depends(get_current_user)):
    print(current_user.get("role"))
    if current_user.get("role") != "UserRole.admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@route.get("/loans",response_model=List[LoanResponse], dependencies=[Depends(require_admin)])
def get_all_loans():
    loanserv=LoanService(session)
    result=loanserv.get_all_loans()
    return result

@route.get("/loans/{loan_id}",response_model=LoanResponse, dependencies=[Depends(require_admin)])
def get_loan_id(loan_id):
    loanserv=LoanService(session)
    result=loanserv.get_loan_by_id(loan_id)
    return result

@route.patch("/loans/{loan_id}/review",response_model=LoanResponse, dependencies=[Depends(require_admin)])
def review_loan(loan_id,review:LoanReview):
    reviewdict=review.model_dump()
    
    loanserv=LoanService(session)
    result=loanserv.review_loan(loan_id,reviewdict)
    return result


@route.get("/loans/userid/{user_id}",response_model=List[LoanResponse],dependencies=[Depends(require_admin)])
def get_loans_user_id(user_id):
    loanserv=LoanService(session)
    result=loanserv.get_loans_userid(user_id)
    return result

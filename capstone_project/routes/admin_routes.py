from fastapi import APIRouter
from services.loan_service import LoanService
from schemas.pyschemas import LoanResponse,LoanReview
from database.models import session
from typing import List

route=APIRouter()

@route.get("/loans",response_model=List[LoanResponse])
def get_all_loans():
    loanserv=LoanService(session)
    result=loanserv.get_all_loans()
    return result

@route.get("/loans/{loan_id}",response_model=LoanResponse)
def get_loan_id(loan_id):
    loanserv=LoanService(session)
    result=loanserv.get_loan_by_id(loan_id)
    return result

@route.patch("/loans/{loan_id}/review",response_model=LoanResponse)
def review_loan(loan_id,review:LoanReview):
    reviewdict=review.model_dump()
    
    loanserv=LoanService(session)
    result=loanserv.review_loan(loan_id,reviewdict)
    return result



    
from fastapi import APIRouter
from schemas.pyschemas import LoanCreate,LoanResponse
from services.loan_service import LoanService
from database.models import session
from typing import List

route=APIRouter()


@route.post("/",status_code=201)
def add_loan_application(loan:LoanCreate):
    loandict=loan.model_dump()
    loanserve=LoanService(session)
    result=loanserve.AddLoan(loandict)
    return result

@route.get("/my/{user_id}",response_model=List[LoanResponse],status_code=200)
def get_loans(user_id):
    loanserve=LoanService(session)
    result=loanserve.view_my_loans(user_id)
    return result

@route.get("/my/{user_id}/loanid/{loan_id}",response_model=LoanResponse,status_code=200)
def get_my_loan(user_id,loan_id):
    loanserve=LoanService(session)
    result=loanserve.get_my_loan(user_id,loan_id)
    return result


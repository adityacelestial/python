from fastapi import APIRouter, Depends, HTTPException
from schemas.pyschemas import LoanCreate,LoanResponse
from services.loan_service import LoanService
from database.models import get_db
from typing import List
from security import get_current_user
from fastapi import Depends


route=APIRouter()



@route.post("/", dependencies=[Depends(get_current_user)])
def add_loan_application(loan: LoanCreate, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    loandict = loan.model_dump()
    loandict["user_id"] = current_user.get("user_id")
    loanserve = LoanService(db)
    result = loanserve.AddLoan(loandict)
    return result

@route.get("/my/{user_id}", response_model=List[LoanResponse], status_code=200, dependencies=[Depends(get_current_user)])
def get_loans(user_id: int, current_user: dict = Depends(get_current_user), status: str = None, limit: int = None, page: int = None, db=Depends(get_db)):
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    loanserve = LoanService(db)
    result = loanserve.view_my_loans(user_id, status=status, limit=limit, page=page)
    return result

@route.get("/my/{user_id}/loanid/{loan_id}", response_model=LoanResponse, status_code=200, dependencies=[Depends(get_current_user)])
def get_my_loan(user_id: int, loan_id: int, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    loanserve = LoanService(db)
    result = loanserve.get_my_loan(user_id, loan_id)
    return result
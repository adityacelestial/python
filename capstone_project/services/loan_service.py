
from database.models import Loan
from database.models import User
from datetime import datetime
class LoanService():
    def __init__(self,session):
        self.session=session
    
    def AddLoan(self,dict):
        user_id=dict["user_id"]
        
        user_out=self.session.query(User).filter_by(id=user_id).first()
        if not user_out:
            return "Error in finding user"
        loan=Loan(user_id=user_out.id,purpose=dict["purpose"],amount=dict["amount"],tenure_months=dict["tenure_months"],employment_status=dict["employment_status"])
        try:
            self.session.add(loan)
            self.session.commit()
            self.session.refresh(loan)
            return loan
        except Exception as e:
            self.session.rollback()
    
    def view_my_loans(self,user_id,status:str=None,limit:int=None,page:int=None):
        
        query=self.session.query(Loan).filter_by(user_id=user_id)
        if status:
            query=query.filter_by(status=status)
        if limit is not None:
            query=query.limit(limit)
        if page is not None:
            query=query.offset(page * limit if limit else 0)
        loans=query.all()
        return loans
        
    def get_my_loan(self,user_id,loan_id):
        
        loans=self.session.query(Loan).filter_by(user_id=user_id,id=loan_id).first()
        
        return loans
    def get_all_loans(self,status:str=None,limit:int=None,page:int=None,sorted_by:str=None,order_by:str=None,user_id:int=None,purpose:str=None,employment_status:str=None):
        query=self.session.query(Loan)
        if status:
            query=query.filter_by(status=status)
        if user_id is not None:
            query=query.filter_by(user_id=user_id)
        if purpose:
            query=query.filter_by(purpose=purpose)
        if employment_status:
            query=query.filter_by(employment_status=employment_status)
        if limit is not None:
            query=query.limit(limit)
        if page is not None:
            query=query.offset(page * limit if limit else 0)
        if sorted_by:
            if order_by == "asc":
                query=query.order_by(getattr(Loan, sorted_by).asc())
            else:
                query=query.order_by(getattr(Loan, sorted_by).desc())
        loans=query.all()
        return loans       
    def get_loan_by_id(self,loan_id):
        output=self.session.query(Loan).filter_by(id=loan_id).first()
        
        return output 
    
    def review_loan(self,loan_id,dict):
        status=dict["status"]
        admin_remarks=dict["admin_remarks"]
        
        loan=self.session.query(Loan).filter_by(id=loan_id).first()
        if(loan is None):
            return f"There is no reord with that given loan_id"
        loan.status=status
        loan.admin_remarks=admin_remarks
        loan.reviewed_by="admin"
        loan.reviewed_at=datetime.now()
        
        try:
            self.session.commit()
            self.session.refresh(loan)
            return loan
        except Exception as e:
            return f"There problem in patching {e}"
    
    def get_loans_userid(self,user_id):
        loans_user=self.session.query(Loan).filter_by(user_id=user_id).all()
        return loans_user
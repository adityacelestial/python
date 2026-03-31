
from database.models import Loan
from database.models import User
from database.enums import Status
from datetime import datetime
from utils.decorators import timer
from services.notification import LogFileNotification
from errors.Errors import MaxPendingLoansError, InvalidLoanReviewError


class LoanService():
    def __init__(self, session):
        self.session = session

    @timer
    def AddLoan(self, dict):
        user_id = dict["user_id"]

        user_out = self.session.query(User).filter_by(id=user_id).first()
        if not user_out:
            return "Error in finding user"

        pending_count = self.session.query(Loan).filter_by(user_id=user_id, status=Status.pending).count()
        if pending_count >= 3:
            raise MaxPendingLoansError("You already have 3 pending loans. Wait for review before applying again.")

        loan = Loan(user_id=user_out.id, purpose=dict["purpose"], amount=dict["amount"], tenure_months=dict["tenure_months"], employment_status=dict["employment_status"])
        try:
            self.session.add(loan)
            self.session.commit()
            self.session.refresh(loan)
            LogFileNotification().send(f"New loan application #{loan.id} by user '{user_out.username}' for {loan.purpose.value} — ₹{loan.amount}")
            return loan
        except Exception as e:
            self.session.rollback()
            raise

    @timer
    def view_my_loans(self, user_id, status: str = None, limit: int = None, page: int = None):
        
        query = self.session.query(Loan).filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if limit is not None:
            query = query.limit(limit)
        if page is not None:
            query = query.offset(page * limit if limit else 0)
        loans = query.all()
        return loans
        
    @timer
    def get_my_loan(self, user_id, loan_id):
        
        loans = self.session.query(Loan).filter_by(user_id=user_id, id=loan_id).first()
        
        return loans

    @timer
    def get_all_loans(self, status: str = None, limit: int = None, page: int = None, sorted_by: str = None, order_by: str = None, user_id: int = None, purpose: str = None, employment_status: str = None):
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
    @timer
    def get_loan_by_id(self, loan_id):
        output = self.session.query(Loan).filter_by(id=loan_id).first()
        
        return output 
    
    @timer
    def review_loan(self, loan_id, dict):
        status=dict["status"]
        admin_remarks=dict["admin_remarks"]
        
        loan = self.session.query(Loan).filter_by(id=loan_id).first()
        if loan is None:
            return f"There is no reord with that given loan_id"

        if loan.status != Status.pending:
            raise InvalidLoanReviewError("Loan has already been reviewed")

        loan.status = status
        loan.admin_remarks = admin_remarks
        loan.reviewed_by = "admin"
        loan.reviewed_at = datetime.now()

        try:
            self.session.commit()
            self.session.refresh(loan)
            LogFileNotification().send(f"Loan #{loan.id} for user '{loan.user_id}' has been {loan.status.value} — notification sent")
            return loan
        except Exception as e:
            self.session.rollback()
            raise
    
    @timer
    def get_loans_userid(self,user_id):
        loans_user=self.session.query(Loan).filter_by(user_id=user_id).all()
        return loans_user
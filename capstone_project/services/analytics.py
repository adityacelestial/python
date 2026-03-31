from database.models import session
from database.models import Loan, User
from database.enums import Status, Purpose, EmploymentStatus


def analysis(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user or user.role != "admin":
        return {"error": "Access denied", "message": "This is restricted to Admins"}

    loans = session.query(Loan).all()

    status_breakdown = {status.value: len([loan for loan in loans if loan.status.value == status.value]) for status in Status}
    purpose_breakdown = {purpose.value: len([loan for loan in loans if loan.purpose.value == purpose.value]) for purpose in Purpose}
    employment_breakdown = {emp.value: len([loan for loan in loans if loan.employment_status.value == emp.value]) for emp in EmploymentStatus}

    amounts = [loan.amount for loan in loans]
    average_loan_amount = sum(amounts) / len(amounts) if amounts else 0
    total_disbursed = sum(loan.amount for loan in loans if loan.status.value == "approved")

    return {
        "Total_no_users": session.query(User).count(),
        "Total_no_loans": len(loans),
        "status_breakdown": status_breakdown,
        "Loans_by_purpose": purpose_breakdown,
        "Loans_by_employment": employment_breakdown,
        "Average_loan_amount": average_loan_amount,
        "Total_disbursed": total_disbursed,
    }
    
    
    
    
    
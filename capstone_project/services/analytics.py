from database.models import session
from database.models import Loan,User
from sqlalchemy import func

def analysis(user_id):
    user=session.query(User).filter_by(id=user_id).first()
    
    print(user.id)
    print(user.role)
    if(user.id!=1):
            return f"This is restricted to Admins"
    allusers=session.query(User).all()
    countusers=len(allusers)
    
    alloans=session.query(Loan).all()
    countloans=len(alloans)
    
    pendingloans=session.query(Loan).filter_by(status='pending').all()
    countpending=len(pendingloans)
    
    approvedloans=session.query(Loan).filter_by(status='approved').all()
    countapproved=len(approvedloans)
    
    rejectedloans=session.query(Loan).filter_by(status="rejected").all()
    countrejected=len(rejectedloans)
    
    dispursed=0
    for approved in approvedloans:
        dispursed+=approved.amount
    
    averagedispursed=dispursed/countloans
    
    purposequery=session.query(Loan.purpose,func.count(user_id).label("count")).group_by(Loan.purpose)
    
    groupedpurpose=purposequery.all()
    purposedict={purpose:count for purpose,count in groupedpurpose}
    employmentquery=session.query(Loan.employment_status,func.count(user_id).label("count")).group_by(Loan.employment_status)
    
    groupedemployment=employmentquery.all()
    employmentquerydict={employment:count for employment,count in groupedemployment}
    
    
    
    
    return {
        "Total_no_users":countusers,
        "Total_no_loans":countloans,
        "Pending":countpending,
        "approved":countapproved,
        "rejected":countrejected,
        "Total_disbursed_amount":dispursed,
        "average_dispursed_amount":averagedispursed,
        "Loans_by_purpose":purposedict,
        "Loans_by_employment":employmentquerydict
    }
    
    
    
    
    
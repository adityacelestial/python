
from database.repo import session
from database.models import User

def create_user(id,name):
    user=User(id=id,name=name)
    try:
        
        session.add(user)
        session.commit()
        return f"The row was inserted succesfully"
    except Exception as e:
        session.rollback()
        return f"The error in the insertion of the user {e}"
    
def get_user_id(id):
    
    try:
        result=session.query(User).filter_by(id=id).all()
        return result
    except Exception as e:
        
        return f"There is an error witht the query{e}"

def get_users():
    
    try:
        result=session.query(User).all()
        return result
    except Exception as e:
        return f"There is an problem with query {e}"
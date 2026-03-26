from database.models import session
from database.models import User
class UserService():
    
    def __init__(self,session):
        self.session=session
    
    def create_user(self,dict):
        user=User(username=dict['username'],email=dict['email'],password=dict["password"],phone=dict["phone"],monthly_income=dict["monthly_income"],role="user")
        try:
            
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            return f"The error {e} "
    def login_user(self,dict):
        
        username=dict["username"]
        password=dict["password"]
        
        result=self.session.query(User).filter_by(username=username,password=password).first()
        print(result.id)
        print(result.username)
        if result is not None:
            return {"message":"Login successful","username":f"{result.username}","role":f"{result.role}"}
        else:
            return {"message":"invalid credentials"}
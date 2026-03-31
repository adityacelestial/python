from database.models import session
from database.models import User
from database.enums import UserRole
from security import create_access_token
from errors.Errors import InvalidCredentialsError, DuplicateUserError


class UserService():
    
    def __init__(self,session):
        self.session=session
    
    def create_user(self,dict):
        existing = self.session.query(User).filter((User.username == dict['username']) | (User.email == dict['email'])).first()
        if existing:
            raise DuplicateUserError("Username or email already exists")

        role_val = dict.get("role", "user")
        role = UserRole(role_val) if not isinstance(role_val, UserRole) else role_val
        user=User(username=dict['username'],email=dict['email'],password=dict["password"],phone=dict["phone"],monthly_income=dict["monthly_income"],role=role)
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise

    def login_user(self,dict):
        
        username=dict["username"]
        password=dict["password"]
        
        result=self.session.query(User).filter_by(username=username,password=password).first()
        if result is not None:
            token_data = {"sub": result.username, "user_id": result.id, "role": str(result.role.value)}
            access_token = create_access_token(token_data)
            return {"message":"Login successful","username":f"{result.username}","role":f"{result.role.value}", "access_token": access_token, "token_type": "bearer"}
        else:
            raise InvalidCredentialsError("Invalid credentials")
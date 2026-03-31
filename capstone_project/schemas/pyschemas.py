from pydantic import BaseModel,Field,EmailStr,validator
from datetime import datetime
from typing import Optional
from database.enums import Purpose,EmploymentStatus,Status
class UserCreate(BaseModel):
    username:str=Field(...,min_length=3,max_length=50)
    email:EmailStr
    password:str=Field(...,min_length=8)
    phone:str=Field(...,pattern=r'^\d{10,15}$')
    monthly_income:int=Field(...,ge=0)
    role:str = Field('user')
    
    @validator('email')
    def validate_email(cls,v):
        if('@' not in v or '.' not in v):
            raise ValueError("Not an email")
        return v

class UserResponse(BaseModel):
    
    
    id:int
    username:str
    email:str
    phone:str
    monthly_income:int
    role:str
    is_active:bool
    created_at:datetime


class UserLogin(BaseModel):
    
    username:str
    password:str
    
class LoanCreate(BaseModel):
    user_id:int
    amount:int=Field(...,gt=0,le=1000000)
    purpose:Purpose
    tenure_months:int=Field(...,ge=6,le=360)
    employment_status:EmploymentStatus

class LoanResponse(BaseModel):
    
    id:int
    user_id:int
    amount:int
    purpose:str
    tenure_months:int
    status:str
    admin_remarks:str|None=None
    reviewed_by:str|None=None
    reviewed_at:Optional[datetime]=None
    applied_at:datetime
    
    model_config={
        "from_attributes":True
    }
    
class LoanReview(BaseModel):
    status:Status
    admin_remarks:str

    @validator('status')
    def status_not_pending(cls, v):
        if v == Status.pending:
            raise ValueError('status must be approved or rejected')
        return v

    @validator('admin_remarks')
    def remarks_length(cls, v):
        if not v or len(v.strip()) < 5 or len(v) > 500:
            raise ValueError('admin_remarks must be between 5 and 500 chars')
        return v.strip()
    
    
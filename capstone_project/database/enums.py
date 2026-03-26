import enum

class UserRole(enum.Enum):
    user='user'
    admin='admin'
    
class Purpose(enum.Enum):
    personal='personal'
    education='education'
    home='home'
    vehicle='vehicle'
    business='business'

class EmploymentStatus(enum.Enum):
    employed="employed"
    self_employed="self_employed"
    unemployed="unemployed"
    student="student"

class Status(enum.Enum):
    pending="pending"
    approved="approved"
    rejected="rejected"

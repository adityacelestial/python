from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum, CheckConstraint, Text, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from database.enums import UserRole, Purpose, EmploymentStatus, Status
from dotenv import load_dotenv
import os
from utils.decorators import retry

load_dotenv()
Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@retry(max_attempts=3)
def verify_connection():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        return True


session = SessionLocal()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String(50),nullable=False,unique=True)
    email=Column(String(120),nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    phone=Column(String(15),nullable=False)
    monthly_income=Column(Integer,nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now(timezone.utc))
    role = Column(Enum(UserRole), nullable=False)

    __table_args__ = (
        CheckConstraint("monthly_income>=0", name="ck_monthly_income_positive"),
        CheckConstraint("char_length(username)>=3", name="ck_username_min_length"),
        CheckConstraint("length(phone) BETWEEN 10 AND 15", name="ck_phone_length"),
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"

class Loan(Base):
    __tablename__="loan"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("user.id"),nullable=False)
    amount=Column(Integer,nullable=False)
    purpose=Column(Enum(Purpose),nullable=False)
    tenure_months=Column(Integer,nullable=False)
    employment_status=Column(Enum(EmploymentStatus),nullable=False)
    status = Column(Enum(Status), default=Status.pending)
    admin_remarks = Column(Text, nullable=True)
    reviewed_by = Column(String(50), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    applied_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    credit_score = Column(Integer, nullable=True, default=None)

    __table_args__ = (
        CheckConstraint("amount>0 AND  amount<=1000000", name="Loan_amount_constraint"),
        CheckConstraint("tenure_months>=6 and tenure_months<=360", name="check_tenure_months"),
    )

    def __repr__(self):
        return f"<Loan id={self.id} user_id={self.user_id} status={self.status}>"


# create tables if missing (for test-run paths where migrations are not applied yet)
Base.metadata.create_all(engine)

        
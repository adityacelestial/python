from sqlalchemy.orm import Session
from models.db_models import User, Task


class SQLAlchemyRepository:

    def __init__(self, db: Session):
        self.db = db

    # USER METHODS
    def create_user(self, username: str):
        user = User(username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users(self):
        return self.db.query(User).all()

    def delete_user(self, username: str):
        user = self.get_user(username)
        if user:
            self.db.delete(user)
            self.db.commit()

    # TASK METHODS
    def create_task(self, task_data: dict):
        task = Task(**task_data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(self):
        return self.db.query(Task).all()

    def update_task(self, task_id: int, update_data: dict):
        task = self.get_task(task_id)
        if task:
            for key, value in update_data.items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
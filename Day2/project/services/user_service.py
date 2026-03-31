from datetime import datetime
from fastapi import HTTPException

class UserService:
    def __init__(self, repo):
        self.repo = repo

    def register(self, user):
        users = self.repo.get_all()

        for u in users:
            if u["username"] == user.username:
                raise HTTPException(status_code=409, detail="Duplicate user")

        data = user.dict()
        data["created_at"] = datetime.utcnow()

        return self.repo.create(data)

    def login(self, user):
        users = self.repo.get_all()

        for u in users:
            if u["username"] == user.username and u["password"] == user.password:
                return {"message": "Login successful"}

        raise HTTPException(status_code=401, detail="Invalid credentials")

    def get_all(self):
        return self.repo.get_all()

    def delete(self, user_id):
        self.repo.delete(user_id)
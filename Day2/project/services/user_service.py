from datetime import datetime
import logging

class UserService:

    def __init__(self, repo):
        self.repo = repo
        self.logger = logging.getLogger("user_service")

    def register(self, user_data):
        users = self.repo.get_all()

        if any(u["username"] == user_data.username for u in users):
            self.logger.warning(f"Duplicate username: {user_data.username}")
            raise Exception("Duplicate user")

        new_user = {
            "id": len(users) + 1,
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password,
            "created_at": datetime.utcnow().isoformat()
        }

        self.repo.save(new_user)
        self.logger.info(f"User '{user_data.username}' registered")
        return new_user
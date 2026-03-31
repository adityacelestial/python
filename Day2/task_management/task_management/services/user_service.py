import hashlib
import logging
from datetime import datetime
from typing import Any, Dict, List

from exceptions.custom_exceptions import (
    DuplicateUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserService:
    """Business logic for user management.

    Depends on BaseRepository (DIP) – any conforming implementation
    can be injected without changing this class.
    """

    def __init__(self, repository: BaseRepository) -> None:
        self._repo = repository

    # ──────────────── helpers ────────────────

    def _find_by_username(self, username: str) -> Dict[str, Any] | None:
        return next(
            (u for u in self._repo.find_all() if u["username"] == username), None
        )

    # ──────────────── public API ────────────────

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        if self._find_by_username(username):
            logger.warning("Duplicate username: '%s'", username)
            raise DuplicateUserError(username)

        user = {
            "username": username,
            "email": email,
            "password": _hash_password(password),
            "created_at": datetime.utcnow().isoformat(),
        }
        saved = self._repo.save(user)
        logger.info("User '%s' registered", username)
        return saved

    def login(self, username: str, password: str) -> Dict[str, Any]:
        user = self._find_by_username(username)
        if not user or user["password"] != _hash_password(password):
            logger.warning("Failed login attempt for username: '%s'", username)
            raise InvalidCredentialsError()
        logger.info("User '%s' logged in", username)
        return user

    def list_users(self) -> List[Dict[str, Any]]:
        return self._repo.find_all()

    def delete_user(self, user_id: int) -> bool:
        if not self._repo.find_by_id(user_id):
            logger.error("User ID %d not found", user_id)
            raise UserNotFoundError(user_id)
        self._repo.delete(user_id)
        logger.info("User ID %d deleted", user_id)
        return True

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from exceptions.custom_exceptions import TaskNotFoundError
from models.enums import TaskPriority, TaskStatus
from repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class TaskService:
    """Business logic for task management.

    Depends on BaseRepository (DIP).
    """

    def __init__(self, repository: BaseRepository) -> None:
        self._repo = repository

    # ──────────────── public API ────────────────

    def create_task(
        self,
        title: str,
        owner: str,
        priority: TaskPriority,
        status: TaskStatus,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        task = {
            "title": title,
            "description": description,
            "status": status.value,
            "priority": priority.value,
            "owner": owner,
            "created_at": now,
            "updated_at": now,
        }
        saved = self._repo.save(task)
        logger.info("Task '%s' created with id=%d", title, saved["id"])
        return saved

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        owner: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        tasks = self._repo.find_all()

        if status:
            tasks = [t for t in tasks if t["status"] == status.value]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority.value]
        if owner:
            tasks = [t for t in tasks if t["owner"] == owner]

        start = (page - 1) * limit
        return tasks[start : start + limit]

    def get_task(self, task_id: int) -> Dict[str, Any]:
        task = self._repo.find_by_id(task_id)
        if not task:
            logger.error("Task ID %d not found", task_id)
            raise TaskNotFoundError(task_id)
        return task

    def update_task(self, task_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Full or partial update – caller controls which fields are present."""
        existing = self.get_task(task_id)  # raises TaskNotFoundError if absent
        # Convert enum values to their string form for JSON storage
        cleaned = {}
        for k, v in updates.items():
            if v is None:
                continue
            cleaned[k] = v.value if hasattr(v, "value") else v
        cleaned["updated_at"] = datetime.utcnow().isoformat()
        updated = self._repo.update(task_id, cleaned)
        logger.info("Task ID %d updated", task_id)
        return updated

    def delete_task(self, task_id: int) -> bool:
        self.get_task(task_id)  # raises if not found
        self._repo.delete(task_id)
        logger.info("Task ID %d deleted", task_id)
        return True

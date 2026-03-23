from datetime import datetime
import logging

class TaskService:

    def __init__(self, repo):
        self.repo = repo
        self.logger = logging.getLogger("task_service")

    def create_task(self, task_data, owner):
        tasks = self.repo.get_all()

        task = {
            "id": len(tasks) + 1,
            "title": task_data.title,
            "description": task_data.description,
            "status": task_data.status,
            "priority": task_data.priority,
            "owner": owner,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        self.repo.save(task)
        self.logger.info(f"Task created: {task['title']}")
        return task
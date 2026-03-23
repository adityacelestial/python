from datetime import datetime

class TaskService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, task, owner):
        data = task.dict()
        data["status"] = "pending"
        data["owner"] = owner
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()

        return self.repo.create(data)

    def get_all(self, filters):
        tasks = self.repo.get_all()

        if filters.get("status"):
            tasks = [t for t in tasks if t["status"] == filters["status"]]

        if filters.get("priority"):
            tasks = [t for t in tasks if t["priority"] == filters["priority"]]

        return tasks

    def get_by_id(self, task_id):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise Exception("Task not found")
        return task

    def update(self, task_id, data):
        return self.repo.update(task_id, data)

    def delete(self, task_id):
        self.repo.delete(task_id)
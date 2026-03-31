import asyncio
from abc import ABC, abstractmethod
from datetime import datetime

class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class ConsoleNotification(NotificationStrategy):
    def send(self, message: str):
        print(f"[notification] {message}")


class LogFileNotification(NotificationStrategy):
    def __init__(self, filename: str = "logs/notifications.log"):
        self.filename = filename

    def send(self, message: str):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()} - {message}\n")


async def async_notify_channel(channel: str, loan_id: int, user_id: int, status: str):
    await asyncio.sleep(0.2)
    return f"{channel} processed loan {loan_id} for user {user_id} status {status}"


async def async_notification_simulation(loan_id: int, user_id: int, status: str):
    channels = ["email", "sms", "push"]
    results = await asyncio.gather(*[async_notify_channel(ch, loan_id, user_id, status) for ch in channels])

    message = f"Loan #{loan_id} status {status} notification sent: " + ", ".join(results)
    LogFileNotification().send(message)
    return results

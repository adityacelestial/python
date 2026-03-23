from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Task Manager API"
    LOG_FILE: str = "logs/app.log"
    TASK_FILE: str = "data/tasks.json"
    USER_FILE: str = "data/users.json"

    model_config = SettingsConfigDict(
        extra="ignore"   
    )

settings = Settings()
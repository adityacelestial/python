from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="TaskManagementAPI", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", alias="LOG_FILE")
    tasks_file: str = Field(default="data/tasks.json", alias="TASKS_FILE")
    users_file: str = Field(default="data/users.json", alias="USERS_FILE")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")

    model_config = {"env_file": ".env", "populate_by_name": True}


settings = Settings()

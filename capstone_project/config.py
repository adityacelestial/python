from pydantic import Field

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings
    from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = Field("LoanHub")
    DEBUG: bool = Field(True)
    DATABASE_URL: str
    LOG_LEVEL: str = Field("INFO")
    POOL_SIZE: int = Field(5)
    MAX_OVERFLOW: int = Field(10)
    ADMIN_USERNAME: str = Field("admin")
    ADMIN_PASSWORD: str = Field("admin1234")
    ADMIN_EMAIL: str = Field("admin@loanhub.com")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

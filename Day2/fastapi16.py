# Q16. Environment Variables and Config 

# Topics: Config, Environment Variables, Pydantic 

# Problem Statement: 

# Create a Settings class using Pydantic's BaseSettings that loads APP_NAME, DEBUG, JSON_DB_PATH, and LOG_LEVEL from a .env file. Use these settings in your FastAPI app startup. 

# Input: 

# # .env file content: 

# APP_NAME=TaskAPI 

# DEBUG=true 

# JSON_DB_PATH=./data/tasks.json 

# LOG_LEVEL=INFO 

# Output: 

# # On app startup: 

# App: TaskAPI | Debug: True | DB: ./data/tasks.json 

# Constraints: 

# Use pydantic-settings package 

# Do NOT hardcode any config values in the source code 

# Load settings using model_config = SettingsConfigDict(env_file=".env") 

# Settings must be a singleton used across the app 

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

# ✅ Settings class
class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    JSON_DB_PATH: str
    LOG_LEVEL: str

    # Load from .env file
    model_config = SettingsConfigDict(env_file=".env")


# ✅ Singleton instance
settings = Settings()

# ✅ FastAPI app
app = FastAPI()


# ✅ Startup event
@app.on_event("startup")
def startup_event():
    print(f"App: {settings.APP_NAME} | Debug: {settings.DEBUG} | DB: {settings.JSON_DB_PATH}")


# Sample route
@app.get("/")
def read_root():
    return {"message": "App is running"}
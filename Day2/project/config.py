import os
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "./data")
LOG_FILE = os.getenv("LOG_FILE", "./logs/app.log")
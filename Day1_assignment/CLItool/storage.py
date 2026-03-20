import json
from logger import log_message

FILE = "users.json"

def load_users():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        log_message("WARNING", "users.json not found. Creating new file.")
        return {"users": []}
    except json.JSONDecodeError:
        log_message("ERROR", "Corrupted JSON file.")
        return {"users": []}


def save_users(data):
    try:
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log_message("ERROR", f"Failed to save users: {e}")
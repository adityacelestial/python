from datetime import datetime

def log_message(level, message):
    try:
        with open("logs.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {level} - {message}\n")
    except Exception as e:
        print("Logging failed:", e)
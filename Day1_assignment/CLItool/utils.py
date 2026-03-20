from storage import load_users, save_users
from logger import log_message


def register_user(username, password):
    if not username or not password:
        print("Inputs cannot be empty")
        return

    data = load_users()

    for user in data["users"]:
        if user["name"] == username:
            print("Duplicate user")
            log_message("WARNING", f"Duplicate registration attempt for '{username}'")
            return

    new_user = {
        "id": len(data["users"]) + 1,
        "name": username,
        "password": password
    }

    data["users"].append(new_user)
    save_users(data)

    print("User registered successfully")
    log_message("INFO", f"User '{username}' registered successfully")


def login_user(username, password):
    data = load_users()

    for user in data["users"]:
        if user["name"] == username and user["password"] == password:
            log_message("INFO", f"User '{username}' logged in successfully")
            return True

    return False


def view_users():
    data = load_users()

    usernames = [user["name"] for user in data["users"]]
    print("Users:", usernames)

    log_message("INFO", "User list accessed")


def delete_user(username):
    data = load_users()

    updated_users = [user for user in data["users"] if user["name"] != username]

    if len(updated_users) == len(data["users"]):
        print("User not found")
        log_message("ERROR", f"Attempt to delete non-existing user '{username}'")
        return

    data["users"] = updated_users
    save_users(data)

    print("User deleted successfully")
    log_message("INFO", f"User '{username}' deleted successfully")
from utils import register_user, login_user, view_users, delete_user
from logger import log_message

MENU = """
1. Register User
2. Login
3. View Users
4. Delete User
5. Exit
"""


def main():
    while True:
        print(MENU)

        try:
            option = int(input("Enter option: "))
        except ValueError:
            print("Invalid input")
            continue

        if option == 1:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            register_user(username, password)

        elif option == 2:
            attempts = 0
            while attempts < 3:
                username = input("Enter username: ")
                password = input("Enter password: ")

                if login_user(username, password):
                    print("Login successful")
                    break
                else:
                    attempts += 1
                    print("Login failed")

                    if attempts < 3:
                        log_message("WARNING", f"Failed login attempt {attempts} for '{username}'")
                    else:
                        log_message("ERROR", f"Account locked for '{username}' after 3 attempts")
                        print("Account locked")

        elif option == 3:
            view_users()

        elif option == 4:
            username = input("Enter username to delete: ").strip()
            if username:
                delete_user(username)
            else:
                print("Username cannot be empty")

        elif option == 5:
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
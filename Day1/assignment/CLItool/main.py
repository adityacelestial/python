from utils import register_user, login_user, view_users, delete_user, user_exists
from logger import log_message

FULL_MENU = """
1. Login
2. View Users
3. Delete User
4. Exit
"""

REGISTER_MENU = """
1. Register
2. Exit
"""


def main():
    username = input("Enter username: ").strip()

    if not user_exists(username):
        print("User does not exist.")
        
        while True:
            print(REGISTER_MENU)

            try:
                option = int(input("Enter option: "))
            except ValueError:
                print("Invalid input")
                continue

            if option == 1:
                password = input("Enter password: ").strip()
                register_user(username, password)
                print("User registered successfully")
                break

            elif option == 2:
                print("Exiting...")
                return

            else:
                print("Invalid option")

    else:
        print(f"Welcome back, {username}!")

        while True:
            print(FULL_MENU)

            try:
                option = int(input("Enter option: "))
            except ValueError:
                print("Invalid input")
                continue

            if option == 1:
                attempts = 0
                while attempts < 3:
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

            elif option == 2:
                view_users()

            elif option == 3:
                delete_user(username)

            elif option == 4:
                print("Exiting...")
                break

            else:
                print("Invalid option")


if __name__ == "__main__":
    main()
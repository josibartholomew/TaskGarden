"""
main.py
--------
Entry point for the TaskGarden application.

This file handles:
- User registration
- User login
- Initializing the TaskGardenController after authentication
- Running the main application loop

It interacts with:
- StorageManager (Singleton): For persistent JSON storage
- User model: For loading and constructing user objects
- TaskGardenController: For running the system after login
"""

from utils.storage import StorageManager
from models.user import User
from controller.taskgarden_controller import TaskGardenController

# Create or retrieve the global StorageManager (Singleton)
storage = StorageManager()


def register_user():
    """
    Register a new user in the system.

    Workflow:
    1. Ask for username and password.
    2. Check if user already exists.
    3. Hash the password and save the new user to storage.
    4. Convert the user dictionary into a User object.

    Returns:
        User | None: A User object on success, None on failure.
    """
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()

    # Prevent duplicate usernames
    if storage.find_user(username):
        print(f"User '{username}' already exists!")
        return None

    # Hash and save
    hashed = storage.hash_password(password)
    user_dict = {"username": username, "password_hash": hashed, "categories": []}

    storage.data["users"].append(user_dict)
    storage.save_data()

    print(f"User '{username}' registered!")
    return User.from_dict(user_dict)


def login_user():
    """
    Authenticate an existing user.

    Workflow:
    1. Ask for username and password.
    2. Look up the user in storage.
    3. Hash the entered password and compare to stored hash.
    4. Load user data into a User object.

    Returns:
        User | None: A User object if authentication succeeds, else None.
    """
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    hashed = storage.hash_password(password)
    user_dict = storage.find_user(username)

    # Validate credentials
    if not user_dict:
        print("Invalid username or password.")
        return None

    if user_dict.get("password_hash") != hashed:
        print("Invalid username or password.")
        return None

    return User.from_dict(user_dict)


def main():
    """
    Main program loop for the TaskGarden system.

    Handles:
    - Login flow
    - Registration flow
    - Launching TaskGardenController for authenticated users
    - Exiting the program

    This loop continues until the user chooses 'Exit'.
    """
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Select option: ").strip()

        # ----------------- LOGIN -----------------
        if choice == "1":
            user = login_user()
            if user:
                controller = TaskGardenController(user)
                controller.run()

        # --------------- REGISTRATION -------------
        elif choice == "2":
            user = register_user()
            if user:
                controller = TaskGardenController(user)
                controller.run()

        # ------------------ EXIT ------------------
        elif choice == "3":
            print("Goodbye!")
            break

        # -------- INVALID INPUT HANDLING ----------
        else:
            print("Invalid choice. Try again.")


# Only run main() when executed directly, not imported
if __name__ == "__main__":
    main()

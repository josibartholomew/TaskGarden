# utils/storage.py
import json
from pathlib import Path
import hashlib

class StorageManager:
    """
    Singleton class responsible for loading, saving, and managing
    persistent JSON storage for TaskGarden.

    The system stores:
        - User accounts (username, hashed password, garden data)
        - Garden and plant-growth data for each user

    The storage file is saved as `taskgarden_data.json` in the project root.
    """
    _instance = None
    DATA_FILE = Path("taskgarden_data.json")  # Path to the persistent storage file

    def __new__(cls):
        """
        Override object creation to ensure only one instance exists.
        Implements the Singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(StorageManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the StorageManager.
        Loads the JSON data only once, even if the class is instantiated multiple times.
        """
        if not hasattr(self, "data"):
            self.data = self._load_data()

    def _load_data(self):
        """
        Load user and garden data from the JSON file.
        If the file does not exist, return a default structure.

        Returns:
            dict: Data loaded from storage or a fresh default structure.
        """
        if self.DATA_FILE.exists():
            with open(self.DATA_FILE, "r") as f:
                return json.load(f)

        # Default structure for new installs
        return {"users": []}

    def save_data(self):
        """
        Save all in-memory data back to the JSON file.
        Creates the file if it doesn’t exist.
        """
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4, default=str)

    def find_user(self, username):
        """
        Look up a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            dict or None: User object if found, otherwise None.
        """
        for user in self.data["users"]:
            if user["username"] == username:
                return user
        return None

    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA-256 for secure storage.

        Args:
            password (str): The raw text password.

        Returns:
            str: The SHA-256 hash of the password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

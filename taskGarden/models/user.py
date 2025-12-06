# models/user.py

from models.category import Category

class User:
    """
    Represents a TaskGarden user and their personal data.

    A user contains:
    - A unique username
    - A hashed password for authentication
    - A collection of task categories, each containing tasks and a plant

    Attributes
    ----------
    username : str
        The unique name identifying the user.
    password_hash : str | None
        A hashed password string. May be None for new/incomplete registrations.
    categories : list[Category]
        The list of Category objects belonging to the user.
    """

    def __init__(self, username, password_hash=None, categories=None):
        """
        Initialize a User instance.

        Parameters
        ----------
        username : str
            The user's login name.
        password_hash : str, optional
            Hashed password for secure storage.
        categories : list[Category], optional
            The user's task categories. Defaults to an empty list.
        """
        self.username = username
        self.password_hash = password_hash
        self.categories = categories if categories is not None else []

    # ------------------- Category Retrieval Methods -------------------

    def get_category(self, name):
        """
        Retrieve a category by its name (case-insensitive).

        Parameters
        ----------
        name : str
            The category name to search for.

        Returns
        -------
        Category | None
            The matching category, or None if not found.
        """
        for c in self.categories:
            if c.name.lower() == name.lower():
                return c
        return None

    def require_category(self, name):
        """
        Retrieve a category, raising an error if it does not exist.

        Parameters
        ----------
        name : str

        Raises
        ------
        ValueError
            If the category does not exist.

        Returns
        -------
        Category
        """
        cat = self.get_category(name)
        if not cat:
            raise ValueError(f"Category '{name}' not found.")
        return cat

    def add_category(self, category):
        """
        Add a new category to the user.

        Parameters
        ----------
        category : Category

        Raises
        ------
        ValueError
            If a category with the same name already exists.
        """
        if self.get_category(category.name):
            raise ValueError(f"Category '{category.name}' already exists.")
        self.categories.append(category)

    # ------------------- Serialization -------------------

    def to_dict(self):
        """
        Convert the User into a serializable dictionary for JSON storage.

        Returns
        -------
        dict
            Includes the username, password hash, and all categories.
        """
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "categories": [c.to_dict() for c in self.categories]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct a User object from a stored dictionary.

        Parameters
        ----------
        data : dict
            Dictionary matching structure returned by to_dict().

        Returns
        -------
        User
            User object with reconstructed Category instances.
        """
        user = cls(
            username=data["username"],
            password_hash=data.get("password_hash")
        )

        # Recreate Category objects
        user.categories = [
            Category.from_dict(cat)
            for cat in data.get("categories", [])
        ]

        return user

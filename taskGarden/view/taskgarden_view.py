# view/taskgarden_view.py
from models.plant import Plant

class TaskGardenView:
    """
    Handles all user-facing output for the TaskGarden CLI application.

    This class is responsible for displaying menus, tasks, and the garden
    visualization. It does not modify data; it only presents it to the user.
    """

    @staticmethod
    def show_menu():
        """
        Display the main menu options for the CLI and get the user's selection.

        Returns:
            str: The user's menu choice (as a string for flexibility).
        """
        print("\n--- TaskGarden Main Menu ---")
        print("1. Add Category")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. View Garden")
        print("5. View Tasks")
        print("6. Exit")
        return input("Select an option: ").strip()

    @staticmethod
    def show_garden(user_data):
        """
        Display the user's garden with plant growth stages.

        Args:
            user_data (dict): Dictionary containing user info and categories.
                Expected structure:
                {
                    "username": str,
                    "categories": [
                        {
                            "name": str,
                            "plant_name": str,
                            "growth_level": int,
                            "tasks": [...]
                        },
                        ...
                    ]
                }

        Notes:
            This method uses the Plant class to convert growth_level into an emoji stage.
        """
        print("\n🌸 Your Emoji Garden 🌸")
        for cat in user_data["categories"]:
            # Use Plant to get the growth stage emoji
            plant = Plant(cat['plant_name'], cat.get('growth_level', 0))
            print(f"{cat['name']}: {plant.display()}")

    @staticmethod
    def show_tasks(user_data):
        """
        Display all tasks for the user, showing completion status and category.

        Args:
            user_data (dict): Dictionary containing user info and categories.
                Expected structure is the same as in `show_garden`.

        Notes:
            Completed tasks are shown with ✅, incomplete tasks with ❌.
        """
        print("\n📝 Your Tasks 📝")
        for cat in user_data["categories"]:
            for task in cat.get("tasks", []):
                status = "✅" if task.get("completed", False) else "❌"
                print(f"{task['name']} ({cat['name']}) - {status}")

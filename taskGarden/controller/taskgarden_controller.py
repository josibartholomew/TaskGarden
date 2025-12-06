"""
taskgarden_controller.py
------------------------
This module defines the TaskGardenController, which manages all interactions
between the user and the TaskGarden system via a command-line interface (CLI).

Responsibilities of the Controller:
- Handle user actions (adding categories, tasks, completing tasks)
- Display the garden and task lists
- Route menu selections to appropriate behaviors
- Ensure user data remains synchronized with persistent JSON storage

This controller acts as the “brain” of the system, connecting:
- User model
- Category model
- Task model
- Plant model
- StorageManager Singleton
"""

from models.user import User
from models.category import Category
from models.task import Task
from models.plant import Plant
from utils.storage import StorageManager


class TaskGardenController:
    """
    Controller for the TaskGarden CLI application.
    Orchestrates user interactions and updates the underlying models.
    """

    def __init__(self, user):
        """
        Initialize the controller with a User object.

        Args:
            user (User): The authenticated user currently using the system.

        Notes:
            - StorageManager is a Singleton, so calling it repeatedly returns
              the same instance.
            - The passed User object already contains categories, tasks,
              and plant growth levels reconstructed from JSON.
        """
        self.storage = StorageManager()
        self.user = user

    # ============================================================
    #                        CATEGORY METHODS
    # ============================================================

    def add_category(self, name, species):
        """
        Create a new task category for the user, each with its own plant.

        Args:
            name (str): Category name chosen by the user.
            species (str): Plant species name for visualization.

        Returns:
            None
        """
        if self.user.get_category(name):
            print("Category already exists.")
            return

        category = Category(name, species)
        self.user.categories.append(category)
        self._save_user()
        print(f"Category '{name}' added.")

    def choose_category(self):
        """
        Display a numbered list of categories and prompt the user to select one.

        Returns:
            Category | None: The selected Category object or None if unavailable.
        """
        if not self.user.categories:
            print("You have no categories. Add one first!")
            return None

        print("\nChoose a category:")
        for idx, cat in enumerate(self.user.categories, start=1):
            print(f"{idx}. {cat.name} ({cat.plant.species})")

        while True:
            try:
                choice = int(input("Enter number: "))
                if 1 <= choice <= len(self.user.categories):
                    return self.user.categories[choice - 1]
                print(f"Enter a number between 1 and {len(self.user.categories)}")
            except ValueError:
                print("Please enter a valid number.")

    # ============================================================
    #                           TASK METHODS
    # ============================================================

    def add_task(self):
        """
        Create a new Task and assign it to a chosen category.

        Returns:
            None
        """
        task_name = input("Task name: ").strip()
        if not task_name:
            print("Task name cannot be empty!")
            return

        category = self.choose_category()
        if not category:
            return

        task = Task(task_name)
        category.add_task(task)
        self._save_user()

        print(f"Task '{task_name}' added to category '{category.name}'.")

    def choose_task(self):
        """
        Display a numbered list of ALL tasks across all categories.

        Returns:
            (Category, Task) | (None, None): Tuple containing:
                - The category the task belongs to
                - The task itself
        """
        all_tasks = []

        # Collect (category, task) pairs
        for cat in self.user.categories:
            for task in cat.tasks:
                all_tasks.append((cat, task))

        if not all_tasks:
            print("No tasks available to complete.")
            return None, None

        print("\nChoose a task to complete:")
        for idx, (cat, task) in enumerate(all_tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{idx}. [{status}] {task.name} (Category: {cat.name})")

        while True:
            try:
                choice = int(input("Enter task number: "))
                if 1 <= choice <= len(all_tasks):
                    return all_tasks[choice - 1]
                print(f"Enter a number between 1 and {len(all_tasks)}")
            except ValueError:
                print("Please enter a valid number.")

    def complete_task(self):
        """
        Complete a user-selected task.

        Behavior:
            - Marks task as completed
            - Grows the category's plant
            - Saves updated user data

        Returns:
            None
        """
        category, task = self.choose_task()
        if not task:
            return

        if task.completed:
            print(f"Task '{task.name}' is already completed.")
            return

        try:
            task.complete()
            category.plant.grow()
            self._save_user()
            print(f"Task '{task.name}' completed! {category.plant.get_stage()}")
        except ValueError as e:
            print(e)

    # ============================================================
    #                           VIEW METHODS
    # ============================================================

    def view_garden(self):
        """
        Display each category and its plant’s current growth stage.

        Returns:
            None
        """
        print("\n--- Your Garden ---")
        for cat in self.user.categories:
            print(f"{cat.name}: {cat.plant.get_stage()}")
        print("------------------\n")

    def view_tasks(self):
        """
        Display all tasks in every category.

        Returns:
            None
        """
        print("\n--- Your Tasks ---")
        for cat in self.user.categories:
            print(f"Category: {cat.name}")
            for task in cat.tasks:
                status = "✅" if task.completed else "❌"
                print(f"  {status} {task.name}")
        print("------------------\n")

    # ============================================================
    #                          SAVE METHOD
    # ============================================================

    def _save_user(self):
        """
        Synchronize the in-memory User object with persistent JSON storage.

        Notes:
            - Searches for the user entry by username.
            - If found, updates its categories list.
            - If not found, creates a new entry.

        Returns:
            None
        """
        for idx, u in enumerate(self.storage.data["users"]):
            if u["username"] == self.user.username:
                self.storage.data["users"][idx]["categories"] = [
                    c.to_dict() for c in self.user.categories
                ]
                break
        else:
            # User not found; create new
            self.storage.data["users"].append({
                "username": self.user.username,
                "categories": [c.to_dict() for c in self.user.categories]
            })

        self.storage.save_data()

    # ============================================================
    #                         MAIN LOOP
    # ============================================================

    def run(self):
        """
        Main program loop for the TaskGarden system.

        Menu Actions:
            1. View garden
            2. View tasks
            3. Add category
            4. Add task
            5. Complete task
            6. Exit

        Returns:
            None
        """
        while True:
            print("1. View Garden")
            print("2. View Tasks")
            print("3. Add Category")
            print("4. Add Task")
            print("5. Complete Task")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.view_garden()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                name = input("Category name: ").strip()
                species = input("Plant Species: ").strip()
                self.add_category(name, species)
            elif choice == "4":
                self.add_task()
            elif choice == "5":
                self.complete_task()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

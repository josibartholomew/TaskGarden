# models/category.py

from models.task import Task
from models.plant import Plant

class Category:
    """
    Represents a task category within the TaskGarden system.

    Each category groups a set of related tasks (e.g., "School", "Fitness")
    and is paired with a Plant object that grows when tasks are completed.

    Attributes
    ----------
    name : str
        The name of the category.
    tasks : list[Task]
        A list of Task objects assigned to this category.
    plant : Plant
        The plant representing this category's progress.
    """

    def __init__(self, name, species):
        """
        Initialize a new Category instance.

        Parameters
        ----------
        name : str
            The category name.
        species : str
            The species/type of plant associated with this category.
        """
        self.name = name
        self.tasks = []                 # list of Task objects
        self.plant = Plant(species)     # each category gets its own plant

    # ------------------- Task Methods -------------------

    def add_task(self, task):
        """
        Add a Task object to the category.

        Parameters
        ----------
        task : Task
            The task to add.
        """
        self.tasks.append(task)

    def get_task(self, task_name):
        """
        Retrieve a task by its name (case-insensitive).

        Parameters
        ----------
        task_name : str
            The name of the task to locate.

        Returns
        -------
        Task or None
            The matching Task object, or None if not found.
        """
        for t in self.tasks:
            if t.name.lower() == task_name.lower():
                return t
        return None

    # ------------------- Serialization -------------------

    def to_dict(self):
        """
        Convert this Category into a serializable dictionary for storage.

        Returns
        -------
        dict
            A JSON-friendly dictionary containing category data.
        """
        return {
            "name": self.name,
            "tasks": [t.to_dict() for t in self.tasks],
            "plant": self.plant.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct a Category object from stored dictionary data.

        Parameters
        ----------
        data : dict
            A dictionary previously created by `to_dict()`.

        Returns
        -------
        Category
            A fully restored Category, including tasks and plant state.
        """
        name = data.get("name", "")
        plant_data = data.get("plant", {})
        tasks_data = data.get("tasks", [])

        # Species is stored in plant_data
        species = plant_data.get("species", "Unknown")

        # Create initial category (creates a default Plant internally)
        category = cls(name=name, species=species)

        # Replace default plant with restored one (keeping growth stage)
        category.plant = Plant.from_dict(plant_data)

        # Restore each task
        for t in tasks_data:
            category.tasks.append(Task.from_dict(t))

        return category

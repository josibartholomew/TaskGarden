# models/task.py

from datetime import datetime

class Task:
    """
    Represents a single task in a user's TaskGarden category.

    Tasks belong to categories and contribute to plant growth when completed.

    Attributes
    ----------
    name : str
        The name/description of the task.
    completed : bool
        Whether the task has been marked as completed.
    completed_date : datetime | None
        The date and time when the task was completed. None if incomplete.
    """

    def __init__(self, name):
        """
        Create a new Task.

        Parameters
        ----------
        name : str
            The title or label for the task.
        """
        self.name = name
        self.completed = False       # a new task starts incomplete
        self.completed_date = None   # no completion timestamp yet

    # ------------------- Task Completion Logic -------------------

    def complete(self):
        """
        Mark the task as completed.

        Raises
        ------
        ValueError
            If the task is already completed.

        Side Effects
        ------------
        - Sets completed to True
        - Records the current timestamp in completed_date
        """
        if self.completed:
            raise ValueError("Task already completed.")

        self.completed = True
        self.completed_date = datetime.now()

    # ------------------- Serialization -------------------

    def to_dict(self):
        """
        Convert the Task into a JSON-storable dictionary.

        Returns
        -------
        dict
            Contains task name, completion status, and ISO-formatted completion time.
        """
        return {
            "name": self.name,
            "completed": self.completed,
            "completed_date": (
                self.completed_date.isoformat() if self.completed_date else None
            ),
        }

    @classmethod
    def from_dict(cls, data):
        """
        Restore a Task object from stored dictionary data.

        Parameters
        ----------
        data : dict
            A dictionary created by `to_dict()`.

        Returns
        -------
        Task
            A fully reconstructed Task with correct completion state.
        """
        task = cls(data["name"])
        task.completed = data.get("completed", False)

        cd = data.get("completed_date")
        if cd:
            task.completed_date = datetime.fromisoformat(cd)

        return task

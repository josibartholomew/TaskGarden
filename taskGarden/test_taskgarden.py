# tests/test_taskgarden_unit.py

import unittest
from models.user import User
from models.category import Category
from models.task import Task
from models.plant import Plant
from utils.storage import StorageManager

class TestPlant(unittest.TestCase):
    """
    Unit tests for the Plant class.
    Verifies growth and stage representation.
    """
    def test_growth(self):
        """
        Test that a Plant grows correctly and returns the expected stage emoji.
        """
        try:
            plant = Plant("🌱")
            assert plant.growth_level == 0  # initial growth level
            plant.grow()
            assert plant.growth_level == 1  # growth level increments
            assert isinstance(plant.get_stage(), str)  # stage is string
            print("test 1 - plant growth - passed!")
        except AssertionError:
            print("test 1 - plant growth - failed!")

class TestTask(unittest.TestCase):
    """
    Unit tests for the Task class.
    Verifies task completion logic and prevents double completion.
    """
    def test_task_completion(self):
        try:
            task = Task("Test Task")
            assert not task.completed  # initially incomplete
            task.complete()
            assert task.completed  # should now be complete
            # completing again should raise ValueError
            try:
                task.complete()
                raise AssertionError("Task completed twice")
            except ValueError:
                pass
            print("test 2 - task completion - passed!")
        except AssertionError:
            print("test 2 - task completion - failed!")

class TestCategory(unittest.TestCase):
    """
    Unit tests for the Category class.
    Verifies task management and serialization.
    """
    def setUp(self):
        """Create a sample Category before each test."""
        self.cat = Category("Work", "🌿")

    def test_add_task(self):
        """Test adding a task to a category."""
        try:
            task = Task("Finish homework")
            self.cat.add_task(task)
            assert len(self.cat.tasks) == 1
            assert self.cat.get_task("Finish homework") == task
            print("test 3 - add task to category - passed!")
        except AssertionError:
            print("test 3 - add task to category - failed!")

    def test_to_from_dict(self):
        """Test serializing and deserializing a category."""
        try:
            task = Task("Read chapter")
            self.cat.add_task(task)
            data = self.cat.to_dict()
            cat2 = Category.from_dict(data)
            assert cat2.name == self.cat.name
            assert len(cat2.tasks) == 1
            assert cat2.plant.growth_level == self.cat.plant.growth_level
            print("test 4 - category to/from dict - passed!")
        except AssertionError:
            print("test 4 - category to/from dict - failed!")

class TestUser(unittest.TestCase):
    """
    Unit tests for the User class.
    Verifies category management and serialization.
    """
    def setUp(self):
        """Create a sample User before each test."""
        self.user = User("testuser")

    def test_add_category(self):
        """Test adding a category to a user and preventing duplicates."""
        try:
            cat = Category("Study", "🌱")
            self.user.add_category(cat)
            assert self.user.get_category("Study") == cat
            # adding duplicate should raise ValueError
            try:
                self.user.add_category(cat)
                raise AssertionError("Duplicate category allowed")
            except ValueError:
                pass
            print("test 5 - add category - passed!")
        except AssertionError:
            print("test 5 - add category - failed!")

    def test_to_from_dict(self):
        """Test serializing and deserializing a user."""
        try:
            cat = Category("Chores", "🌿")
            self.user.add_category(cat)
            data = self.user.to_dict()
            user2 = User.from_dict(data)
            assert user2.username == self.user.username
            assert len(user2.categories) == 1
            assert user2.categories[0].name == "Chores"
            print("test 6 - user to/from dict - passed!")
        except AssertionError:
            print("test 6 - user to/from dict - failed!")

class TestStorageManager(unittest.TestCase):
    """
    Unit test for the StorageManager singleton.
    Verifies that only one instance exists.
    """
    def test_singleton(self):
        try:
            sm1 = StorageManager()
            sm2 = StorageManager()
            assert sm1 is sm2  # same instance
            print("test 7 - storage singleton - passed!")
        except AssertionError:
            print("test 7 - storage singleton - failed!")

if __name__ == "__main__":
    # Run all tests with minimal verbosity (no dots)
    unittest.main(verbosity=0)

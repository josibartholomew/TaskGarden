# TaskGarden
# TaskGarden

TaskGarden is a command-line productivity and habit-tracking application designed to help users grow tasks like plants. Categories, tasks, and virtual plants work together to create a fun, garden-themed workflow.

## Features

* **User Profiles** – Create and store user information.
* **Categories** – Organize tasks into meaningful groups.
* **Tasks** – Add, complete, and manage tasks.
* **Plants** – Each plant grows as tasks in its category are completed.
* **Storage Manager** – Handles saving and loading data.
* **CLI-Based Interface** – A simple, text-driven interface for interacting with the system.

## Project Structure

```
models/
  user.py
  category.py
  task.py
  plant.py
utils/
  storage.py
tests/
  test_taskgarden_unit.py
main.py
```

## Installation

Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd taskGarden
   ```

## Usage

Run the main program:

```bash
python main.py
```

Follow the on-screen prompts to manage users, categories, tasks, and plants.

## Running Tests

```bash
python -m unittest tests/test_taskgarden_unit.py
```

## Notes

* This project was originally planned as a full mobile app, but Stage 1 was implemented as a CLI version instead.
* The structure is modular, making it easier to expand into future GUI or mobile implementations.

## License

This project is provided as-is for educational use.

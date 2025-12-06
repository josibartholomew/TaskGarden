# DESIGN.md

## System Architecture Overview

TaskGarden is structured around a modular, object-oriented architecture designed for clarity, extensibility, and ease of testing. Although the long-term goal was a full mobile app, this stage of the project focuses on a clean, maintainable CLI implementation that models core logic independently of any user interface.

### High-Level Architecture

```
+---------------------+
|       main.py       |  ← CLI controller
+----------+----------+
           |
           v
+---------------------+        +------------------+
|       models        | <----> |   storage.py     |
| User | Category | Task |     | (StorageManager) |
| Plant                |        +------------------+
+---------------------+

+---------------------+
|        tests        |
+---------------------+
```

---

## Major Classes

### **User**

Represents an individual user of the system. Manages personal info and connections to categories.

* **Responsibilities:**

  * Store username and metadata
  * Track categories owned by the user

### **Category**

A grouping mechanism for tasks. Each Category is paired with a Plant for a gamified experience.

* **Responsibilities:**

  * Hold a list of tasks
  * Contain an associated Plant instance
  * Report progress based on completed tasks

### **Task**

Represents an individual actionable item.

* **Attributes:** description, due date, status (complete/incomplete)
* **Responsibilities:**

  * Mark tasks as completed
  * Provide status for reporting and growth calculations

### **Plant**

The playful visual metaphor at the heart of TaskGarden.

* **Responsibilities:**

  * Track growth level
  * Update growth based on completed tasks within its Category
  * Provide emoji-based visual representation (e.g., seed → sprout → full plant)

### **StorageManager** (utils/storage.py)

Handles persistence.

* **Responsibilities:**

  * Save objects to disk (likely JSON)
  * Load data at program start
  * Ensure data integrity across sessions

---

## Design Decisions

### **1. CLI First, Mobile Later**

Originally the project was intended as a full mobile application. However, to focus on core logic, I implemented Stage 1 as a command-line interface. This allowed me to:

* Build robust data models first
* Decouple UI from logic
* Ensure tests could run without UI complexity

### **2. Object-Oriented Modeling**

Each real-world concept (task, category, user, plant) is modeled as its own class. Benefits include:

* Clear separation of concerns
* Easier future expansion (e.g., adding a GUI wrapper)
* Straightforward unit testing

### **3. Gamification Through Plants**

Plants grow as tasks are completed. This introduces:

* Motivation for users
* A sense of progress
* A unique aesthetic direction designed to carry into a future mobile app

### **4. Storage Abstraction**

All saving and loading is handled by `StorageManager`. This abstraction lets the rest of the system ignore whether data is stored via:

* JSON
* SQLite
* Cloud backend (future mobile expansion)

This improves modularity and future adaptability.

---

## Challenges Faced

### **Shifting from App to CLI**

Transitioning from a mobile-app mindset to a CLI required rethinking user interactions. Mobile UX patterns don’t translate 1:1 into text prompts. I had to redesign workflows to be clear and linear.

### **Deciding What to Implement Now vs. Later**

Since only Stage 1 was due, I disciplined myself to implement core logic and models without getting sidetracked by UI or extra features.

### **Data Persistence**

Ensuring clean serialization/deserialization of nested objects (Users → Categories → Tasks → Plants) was complex and required careful structure.

### **Plant Growth Logic**

I wanted growth to feel meaningful without being overcomplicated. Designing a simple but satisfying growth progression took iteration.

---

## What I Learned

* The importance of **planning architecture early**, especially when a long-term mobile or GUI version is planned.
* How **object-oriented design** helps keep a project organized and scalable.
* The value of **testable core logic**, especially when UI layers will change later.
* How to use the CLI as a prototyping tool for validating system behavior.

---

## Future Improvements

### **1. Full Mobile App (Original Vision)**

Using React Native, Flutter, or Kotlin/Swift would unlock:

* Touch interactions
* Visual plant growth animations
* Notifications for incomplete tasks

### **2. More Plant Types**

Unique plants per category (flowers, trees, vines) to increase personalization.

### **3. Better Storage**

Move from JSON to SQLite or cloud sync.

### **4. Analytics Dashboard**

Daily/weekly summaries, task streaks, productivity graphs.

### **5. Accessibility Features**

* Colorblind-friendly themes
* Screen reader support

---

## Conclusion

TaskGarden’s architecture balances simplicity with future extensibility. By focusing this stage on a solid, well-tested core—while decoupling UI entirely—the system is prepared for future transformation into a polished mobile app or graphical desktop interface.

import json
from typing import List


class Task:
    def __init__(self, description: str, completed: bool = False):
        self.description = description
        self.completed = completed


class ToDoList:
    def __init__(self, filename: str = "Tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    task = Task(item["description"], item["completed"])
                    self.tasks.append(task)
        except FileNotFoundError:
            print("No previous tasks found. Starting fresh! :)")
        except json.JSONDecodeError:
            print("Corrupted data file. Starting with empty list.")

    def save_tasks(self):
        data = [
            {"description": task.description, "completed": task.completed}
            for task in self.tasks
        ]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_task(self, description: str):
        if not description.strip():
            print("Cannot add an empty task!")
            return
        self.tasks.append(Task(description.strip()))
        print(f"Task added: {description} ✅")
        self.save_tasks()

    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet. Add one! 📝")
            return
        print("\n" + "=" * 15 + " TASK LIST " + "=" * 15)
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "○"
            print(f"{i}. {status} {task.description}")
        print("=" * 42)

    def complete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            print(f"Completed: {self.tasks[index].description} 🎉")
            self.save_tasks()
        else:
            print("Invalid task number!")

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"Deleted: {removed.description} 🗑️")
            self.save_tasks()
        else:
            print("Invalid task number!")

    def clear_tasks(self):
        self.tasks.clear()
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f)
        print("All tasks cleared! 🧹")


if __name__ == "__main__":
    print("Welcome to Your Smart To-Do List! 📔")
    todo = ToDoList()
    todo.show_tasks()

    while True:
        print("\n1. Add task")
        print("2. Show tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Clear all tasks")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            while True:
                desc = input("Enter task description: ").strip()
                if desc:
                    todo.add_task(desc)
                else:
                    print("Empty task skipped.")

                if input("Add another task? (y/n): ").strip().lower() != "y":
                    break

        elif choice == "2":
            todo.show_tasks()

        elif choice == "3":
            todo.show_tasks()
            try:
                idx = int(input("Enter task number to complete: ")) - 1
                todo.complete_task(idx)
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "4":
            todo.show_tasks()
            try:
                idx = int(input("Enter task number to delete: ")) - 1
                todo.delete_task(idx)
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "5":
            if todo.tasks:
                confirm = (
                    input("Are you sure you want to clear ALL tasks? (y/n): ")
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    todo.clear_tasks()
            else:
                print("No tasks to clear!")

        elif choice == "6":
            print("Goodbye! See you soon! 👋")
            break

        else:
            print("Invalid choice. Try again!")
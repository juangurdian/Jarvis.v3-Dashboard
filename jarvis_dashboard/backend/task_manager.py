# task_manager.py
import datetime
import uuid
import json
import os

# Define the path for the persistent storage file
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file; return an empty list if the file doesn't exist."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                tasks = json.load(f)
                print("[TASK_MANAGER] Loaded tasks:", tasks)
                return tasks
        except Exception as e:
            print("[TASK_MANAGER] Error loading tasks:", e)
    return []

def save_tasks(tasks):
    """Save the tasks list to the JSON file."""
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
            print("[TASK_MANAGER] Saved tasks:", tasks)
    except Exception as e:
        print("[TASK_MANAGER] Error saving tasks:", e)

def add_task(description, due_date, status="not started"):
    task = {
        "id": str(uuid.uuid4()),
        "description": description,
        "due_date": due_date,
        "status": status,
        "created_at": datetime.datetime.now().isoformat()
    }
    tasks = load_tasks()  # Load current tasks
    tasks.append(task)
    print("[TASK_MANAGER] Added task:", task)
    save_tasks(tasks)
    return task

def get_tasks():
    """Always load and return tasks from the JSON file."""
    return load_tasks()

def update_task(task_id, description=None, due_date=None, status=None):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if description is not None:
                task["description"] = description
            if due_date is not None:
                task["due_date"] = due_date
            if status is not None:
                task["status"] = status
            print("[TASK_MANAGER] Updated task:", task)
            save_tasks(tasks)
            return task
    return None

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) < len(tasks):
        print("[TASK_MANAGER] Deleted task with ID:", task_id)
        save_tasks(new_tasks)
        return True
    else:
        print("[TASK_MANAGER] Task not found for deletion, ID:", task_id)
        return False

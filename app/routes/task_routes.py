from flask import Blueprint, jsonify, request
from ..models.task import Task
from ..db import db

# Create a Blueprint for Task routes.
tasks_bp = Blueprint("tasks", __name__)


# Get all tasks.
@tasks_bp.get("/tasks")
def get_all_tasks():
    tasks = db.session.scalars(db.select(Task)).all()

    # Convert each Task object into a dictionary.
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200


# Create a new task.
@tasks_bp.post("/tasks")
def create_task():
    task_data = request.get_json()

    # Check that title and description are present.
    if not isinstance(task_data, dict) or "title" not in task_data or "description" not in task_data:
        return jsonify({"details": "Invalid data"}), 400

    # Create a Task object from the request data.
    new_task = Task.from_dict(task_data)

    # Save the task in the database.
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


# Get one task by its ID.
@tasks_bp.get("/tasks/<int:task_id>")
def get_one_task(task_id):
    # Find the task in the database.
    task = db.session.get(Task, task_id)

    # Return an error if the task does not exist.
    if task is None:
        return jsonify({"details": "Task not found"}), 404

    # Return the task as JSON.
    return jsonify(task.to_dict()), 200


# Update an existing task.
@tasks_bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    # Find the task in the database.
    task = db.session.get(Task, task_id)

    # Return an error if the task does not exist.
    if task is None:
        return jsonify({"details": "Task not found"}), 404

    task_data = request.get_json()

    # Check that title and description are present.
    if not isinstance(task_data, dict) or "title" not in task_data or "description" not in task_data:
        return jsonify({"details": "Invalid data"}), 400

    # Update the task fields.
    task.title = task_data["title"]
    task.description = task_data["description"]

    # Save the changes in the database.
    db.session.commit()

    return "", 204



# Delete a task
@tasks_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    # Find the task in the database.
    task = db.session.get(Task, task_id)

    # Return an error if the task does not exist.
    if task is None:
        return jsonify({"details": "Task not found"}), 404

    # Delete the task from the database.
    db.session.delete(task)

    # Save the change.
    db.session.commit()

    return "", 204


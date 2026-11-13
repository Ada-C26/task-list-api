from flask import Blueprint, jsonify, request
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from .route_utilities import create_model, validate_model

# Create a Blueprint for Goal routes.
goals_bp = Blueprint("goals", __name__)

# Define a route to get all goals.
@goals_bp.get("/goals")
def get_goals():
    goals = db.session.scalars(db.select(Goal)).all()
    return jsonify([goal.to_dict() for goal in goals])

# Define a route to create a new goal.
@goals_bp.post("/goals")
def create_goal():
    goal_data = request.get_json()

    response = create_model(Goal, goal_data)

    return jsonify(response[0]), response[1]


# Define a route to get a goal by its ID.
@goals_bp.get("/goals/<int:goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict())

# Define a route to update a goal by its ID.
@goals_bp.put("/goals/<int:goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_data = request.get_json()
    goal.title = goal_data["title"]

    db.session.commit()

    return jsonify({}), 204

# Define a route to delete a goal by its ID.
@goals_bp.delete("/goals/<int:goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({}), 204


# Add tasks to a goal.
@goals_bp.post("/goals/<int:goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_data = request.get_json()

    # Check if task_ids is in the request.
    if not task_data or "task_ids" not in task_data:
        return jsonify({"details": "Invalid data"}), 400

    task_ids = task_data["task_ids"]

    # Find all tasks with these IDs.
    tasks = db.session.scalars(
        db.select(Task).where(Task.id.in_(task_ids))
    ).all()

    # Check if all requested tasks exist.
    if len(tasks) != len(task_ids):
        return jsonify({"details": "Task not found"}), 404

    # Replace the current tasks with the new tasks.
    goal.tasks = tasks

    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }), 200


# Get a goal and all its tasks.
@goals_bp.get("/goals/<int:goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    })
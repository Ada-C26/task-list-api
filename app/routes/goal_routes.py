from flask import Blueprint, jsonify, request
from ..models.goal import Goal
from ..db import db

# Create a Blueprint for Goal routes.
goals_bp = Blueprint("goals", __name__)

# Define a route to get all goals.
@goals_bp.get("/goals")
def get_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

# Define a route to create a new goal.
@goals_bp.post("/goals")
def create_goal():
    goal_data = request.get_json()

    # Check if the title is missing.
    if not goal_data or "title" not in goal_data:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(goal_data)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201

# Define a route to get a goal by its ID.
@goals_bp.get("/goals/<int:goal_id>")
def get_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None:
        return jsonify({"details": "Goal not found"}), 404
    return jsonify(goal.to_dict())

# Define a route to update a goal by its ID.

@goals_bp.put("/goals/<int:goal_id>")
def update_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if goal is None:
        return jsonify({"details": "Goal not found"}), 404

    goal_data = request.get_json()
    goal.title = goal_data["title"]

    db.session.commit()

    return jsonify({}), 204

# Define a route to delete a goal by its ID.
@goals_bp.delete("/goals/<int:goal_id>")
def delete_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None:
        return jsonify({"details": "Goal not found"}), 404
    db.session.delete(goal)
    db.session.commit()
    return jsonify({}), 204
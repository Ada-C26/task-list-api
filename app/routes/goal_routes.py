from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.route_utilities import validate_model, create_model_with_response, get_models_with_filters_with_response
bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Wave 5: Create a new goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_with_response(Goal, request_body)

# Wave 5: Get all goals
@bp.get("")
def get_all_goals():
    return get_models_with_filters_with_response(Goal, request.args)

# Wave 5: Get one goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()

# Wave 5: Update a goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    if not request_body or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# Wave 5: Delete a goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# Wave 6: Associate tasks with a goal
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    if not request_body or "task_ids" not in request_body:
        return {"details": "Invalid data"}, 400

    task_ids = request_body["task_ids"]

    tasks = [validate_model(Task, task_id) for task_id in task_ids]

    goal.tasks = tasks

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200

# Wave 6: Get all tasks belonging to a goal
@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }, 200
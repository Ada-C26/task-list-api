from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model, get_models_with_filters
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# CREATE a goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

# READ goals
@bp.get("")
def get_all_goals():
    sort = request.args.get("sort")
    return get_models_with_filters(Goal, sort=sort)

# READ a goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

# UPDATE a goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE a goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# CREATING NESTED ROUTES

# ADD existing tasks to a specific goal
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.get_json()["task_ids"]

    tasks = [validate_model(Task, task_id) for task_id in task_ids]

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

# READ all tasks from a specific goal
@bp.get("/<goal_id>/tasks")
def get_all_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict
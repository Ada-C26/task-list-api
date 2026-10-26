from sqlalchemy import func
from datetime import datetime
from flask import Blueprint, request, Response, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .route_utilities import (
    validate_model, 
    create_model, 
    update_model, 
    get_models_with_filters, 
    quiet_success_response, 
    send_slack_notification
)

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.get("")
def get_all_goals():
    goals_response = get_models_with_filters(Goal, request.args)
    return goals_response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    this_goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    return update_model(this_goal, request_body)

@goals_bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return quiet_success_response()

@goals_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids", [])

    try:
        task_ids = [int(tid) for tid in task_ids]
    except (ValueError, TypeError):
        abort(make_response({"details": "Invalid data"}, 400))

    task_ids_set = set(task_ids)

    tasks_query = db.select(Task).where(
        Task.id.in_(task_ids_set)
    )

    tasks = db.session.scalars(tasks_query).all()

    goal.tasks = tasks

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

    return response

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = goal.tasks

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }

    return response
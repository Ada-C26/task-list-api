from flask import Blueprint
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from flask import request, Response
from .route_utilities import create_model, delete_model, get_models_with_filters, update_model, validate_model

bp = Blueprint("goal", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.post("/<goal_id>/tasks")
def create_task_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    # Clear existing associations
    for task in goal.tasks:
        task.goal_id = None
    
    task_ids = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        task_ids.append(task_id)
    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}


@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    return validate_model(Goal, goal_id).to_dict()

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal= validate_model(Goal, goal_id)

    response = goal.to_dict()

    if not goal.tasks:
        response["tasks"] = []

    return response

@bp.put("/<goal_id>")
def update_goal(goal_id):
    return update_model(Goal, goal_id, request.get_json())

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    return delete_model(Goal, goal_id)



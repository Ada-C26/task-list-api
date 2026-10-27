from flask import Blueprint, request, Response
from ..models.goal import Goal
from ..models.task import Task
from ..routes.route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():

    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return Response("Title is required", 400)

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def send_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    new_task_list = [validate_model(Task, task_id) for task_id in request_body["task_ids"]]
    
    goal.tasks = new_task_list
    
    db.session.commit()    

    response = {
        "id" : goal.id,
        "task_ids" : request_body["task_ids"]
    }

    return response

@bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(include_tasks=True)





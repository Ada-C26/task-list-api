from flask import Blueprint,request,Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model,create_model,get_models_with_filters
from ..db import db

bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal,request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal,request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype ="application/json")

@bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def create_task_ids_for_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids",[])

    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task,task_id)
        task.goal_id = goal.id
    db.session.commit()
    return {
        "id" : goal.id,
        "task_ids" : [task.id for task in goal.tasks]
    },200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict,200

    


        
    










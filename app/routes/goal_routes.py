from flask import Blueprint, request, Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import validate_model, create_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

'''Wave 5 CRUD Routes'''

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)
    return [goal.to_dict() for goal in goals]


@bp.get("/<goal_id>")
def get_one_task(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


'''Wave 6 Routes'''
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    tasks = [validate_model(Task, task_id)
            for task_id in request_body["task_ids"]]

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = goal.to_dict()
    response["tasks"] = [task.to_dict() for task in goal.tasks]
    return response

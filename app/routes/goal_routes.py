from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from app.routes.routes_utilities import validate_model, create_model

goals_bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@goals_bp.post("")
def create_new_goal():
    request_body = request.get_json(silent=True)
    if not isinstance(request_body, dict) or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    return create_model(Goal, request_body)

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goal_list = db.session.scalars(query)

    goal_response = []
    for goal in goal_list:
        goal_response.append(goal.to_dict())

    return goal_response, 200


@goals_bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goals_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks    
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    
    response = goal.to_dict()
    
    response["tasks"] = [
        task.to_dict(include_goal_id=True)
        for task in goal.tasks
    ]
    
    return response, 200    

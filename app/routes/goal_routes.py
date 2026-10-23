from flask import Blueprint, abort, make_response, request, Response
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import (
    create_model,
    validate_model,
    get_models_with_filters,
)

bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.get("")
def get_all_goals():
    goals = get_models_with_filters(Goal, request.args)

    return goals


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()


@bp.post("")
def create_goal():
    request_body = request.get_json()
    goal = create_model(Goal, request_body)

    return goal


@bp.put("/<goal_id>")
def edit_goal(goal_id):
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


@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks],
    }
    return response


@bp.post("/<goal_id>/tasks")
def create_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    tasks = [validate_model(Task, task_id) for task_id in request_body["task_ids"]]

    goal.tasks = tasks
    db.session.commit()

    response = {"id": goal.id, "task_ids": [task.id for task in goal.tasks]}

    return response

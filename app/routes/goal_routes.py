from flask import Blueprint, make_response, request, Response
from app.db import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import (
    create_model,
    validate_model,
    get_models_with_filters_with_response,
)


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json(silent=True)
    goal = create_model(Goal, request_body)

    return goal.to_dict(), 201


@bp.get("")
def get_all_goals():
    return get_models_with_filters_with_response(Goal, request.args)


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        return {"details": "Invalid data"}, 400

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
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not isinstance(
        request_body.get("task_ids"), list
    ):
        return {"details": "Invalid data"}, 400

    tasks = []

    for task_id in request_body["task_ids"]:
        if type(task_id) is not int:
            return {"details": "Task IDs must be integers"}, 400

        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks],
    }, 200


@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict, 200

from flask import Blueprint, Response, request
from app.db import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import create_model, validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.get("")
def get_goals():
    goals = db.session.scalars(db.select(Goal)).all()
    return [goal.to_dict() for goal in goals]


@bp.get("/<int:goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()


@bp.post("")
def create_goal():
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        return {"details": "Invalid data"}, 400

    return create_model(Goal, request_body)


@bp.put("/<int:goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        return {"details": "Invalid data"}, 400

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<int:goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<int:goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not isinstance(
        request_body.get("task_ids"), list
    ):
        return {"details": "Invalid data"}, 400

    task_ids = request_body["task_ids"]
    tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks],
    }


@bp.get("/<int:goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if goal is None:
        return {"message": "Goal not found"}, 404

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks],
    }

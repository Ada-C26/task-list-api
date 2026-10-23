from flask import Blueprint, request, Response
from app import db
from app.models.task import Task
from app.routes.route_utilities import (
    create_model,
    validate_model,
    get_models_with_filters,
    send_message,
)
from datetime import datetime

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.get("")
def get_all_tasks():
    tasks = get_models_with_filters(Task, request.args)
    return tasks


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()


@bp.post("")
def create_task():
    request_body = request.get_json()
    response = create_model(Task, request_body)
    return response


@bp.put("/<task_id>")
def edit_task(task_id):

    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    task.is_complete = request_body.get("is_complete")
    task.goal_id = request_body.get("goal_id")
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):

    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    send_message(task.title)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

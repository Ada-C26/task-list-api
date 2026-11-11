from flask import Blueprint, request, Response
from app.models.task import Task
from app.db import db
from datetime import datetime

from app.slack_utilities import send_slack_notification

from app.route_utilities import get_models_with_filters_with_response, validate_model, create_model_with_response

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# Wave 1 and Wave 7: Create a new task using helper
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model_with_response(Task, request_body)


# Wave 1 and Wave 2: Get all tasks with sorting
@bp.get("")
def get_all_tasks():
    return get_models_with_filters_with_response(Task, request.args)

# Wave 1: Get one task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()


# Wave 1: Update a task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Wave 1: Delete a task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Wave 3: Mark a task incomplete
@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Wave 3 and Wave 4: Mark a task complete and notify Slack
@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    send_slack_notification(task)

    return Response(status=204, mimetype="application/json")
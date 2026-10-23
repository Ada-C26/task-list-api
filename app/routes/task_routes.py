from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model, get_models_with_filters
from app.models.task import Task
from datetime import datetime
from ..db import db
import os, requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# CREATE a task
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

# READ tasks
@bp.get("")
def get_all_tasks():
    filters = {}

    if request.args.get("title"):
        filters["title"] = request.args.get("title")
    sort = request.args.get("sort")

    return get_models_with_filters(Task, filters, sort)

# READ a task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

# UPDATE a task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE a task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# CREATING CUSTOM ENDPOINTS

# Mark Complete on an Incomplete/Complete Task
@bp.patch("/<task_id>/mark_complete")
def update_task_marking_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    slackbot_token = os.environ.get("SLACKBOT_API_KEY")

    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {slackbot_token}",
            "Content-Type": "application/json"
        },
        json={
            "channel": "task-notifications-c26",
            "text": f"Someone just completed the task {task.title}"
        }
    )

    return Response(status=204, mimetype="application/json")

# Mark Incomplete on an Incomplete/Complete Task
@bp.patch("/<task_id>/mark_incomplete")
def update_task_marking_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

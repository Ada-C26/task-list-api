from flask import Blueprint, request, Response
from ..models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
import os, requests, logging

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():

    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body and "description" not in request_body:
        return Response("Title and Description are required", 400)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def patch_task_mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.mark_complete()

    db.session.commit()
    notify_slack(task.title)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.mark_incomplete()

    db.session.commit()

    return Response(status=204, mimetype="application/json")

logger = logging.getLogger(__name__)

def notify_slack(task_title):

    token = os.environ.get("SLACK_BOT_TOKEN")
    slack_api_url = os.environ.get("SLACK_API_URL")

    if not token:
        logger.warning("SLACK_BOT_TOKEN is not set in environment variables")
        return

    headers = {"Authorization": f"Bearer {token}"}

    body = {
    "channel": "task-notifications-c26",
    "text": f"Someone just completed the task {task_title}"
    }

    try:
        response = requests.post(slack_api_url, headers=headers, json=body, timeout=5)

        response.raise_for_status()
    
    except requests.exceptions.RequestException as error:
        logger.error(f"Failed to send Slack notification for task '{task_title}': {error}")

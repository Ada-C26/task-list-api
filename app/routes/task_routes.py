import os
import requests
from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model, delete_model, get_models_with_filters, update_model
from datetime import datetime
from ..models.task import Task
from ..db import db

bp = Blueprint('task', __name__, url_prefix='/tasks')

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():    
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    return validate_model(Task, task_id).to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    # Enhancements: Handle non-datetime values for completed_at by setting them to None
    if request.get_json().get("completed_at") and not isinstance(request.get_json().get("completed_at"), datetime):
        request.get_json()["completed_at"] = None
    return update_model(Task, task_id, request.get_json())

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    
    slack_data = {
        "channel": os.environ.get("SLACK_CHANNEL"),
        "text": f"Someone just completed the task {task.title}"
    }
    slack_headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=slack_headers,
        json=slack_data
    )

    return Response(status=204, mimetype='application/json')

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype='application/json')

@bp.delete("/<task_id>")
def delete_task(task_id):
    return delete_model(Task, task_id)
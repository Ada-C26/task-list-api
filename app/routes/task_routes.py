from datetime import datetime
from flask import Blueprint, request, Response, make_response, abort
from app.models.task import Task
from ..db import db
from .route_utilities import (
    validate_model, 
    create_model, 
    update_model, 
    get_models_with_filters, 
    quiet_success_response, 
    send_slack_notification
)

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_all_tasks():
    tasks_response = get_models_with_filters(Task, request.args)
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict(), 200

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    this_task = validate_model(Task, task_id)
    request_body = request.get_json()
    return update_model(this_task, request_body)

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return quiet_success_response()

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_as_complete(task_id):
    this_task = validate_model(Task, task_id)

    update = {"completed_at": datetime.now()}

    result = update_model(this_task, update)

    send_slack_notification("#task-notifications-c26", f"Someone just completed the task {this_task.title}")

    return result

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_as_incomplete(task_id):
    this_task = validate_model(Task, task_id)

    update = {"completed_at": None}

    return update_model(this_task, update)
from flask import Blueprint, request, Response 
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
from datetime import datetime
import os
import requests




bp = Blueprint("tasks_bp",__name__,url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task,request_body)

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    

    db.session.commit()

    return Response(status= 204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task,task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status= 204, mimetype= "application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task,task_id)
    
    if task.completed_at is None:
        task.completed_at = datetime.now()
        db.session.commit()

        slack_token = os.environ.get("SLACK_BOT_TOKEN")
        slack_channel = os.environ.get("CHANNEL_ID")
        

        headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8"
        }

        payload = {
        "channel": slack_channel,
        "text": f"Someone just completed the task {task.title} "
        }

        requests.post("https://slack.com/api/chat.postMessage", headers=headers, json = payload)

    return Response(status = 204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = None
    
    db.session.commit()
    return Response(status = 204, mimetype="application/json")
    
        



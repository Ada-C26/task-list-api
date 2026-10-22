from flask import Blueprint, request, Response, abort, make_response
from app.models.task import Task
from ..db import db
from datetime import datetime, timezone
import os
import requests
from app.routes.routes_utilities import validate_model, create_model

tasks_bp = Blueprint("tasks_bp",__name__,url_prefix="/tasks")

@tasks_bp.post("")
def create_new_task():
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict):
        return {"details": "Invalid data"}, 400

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    

    return create_model(Task, request_body)


@tasks_bp.get("")
def get_all_task():
    sort_query = request.args.get("sort")

    query = db.select(Task)
    if sort_query == 'asc':
        query = query.order_by(Task.title.asc())
    elif sort_query == 'desc':
        query = query.order_by(Task.title.desc())    
    else:
        query = query.order_by(Task.id)    

    tasks_list = db.session.scalars(query)

    task_response = []
    for task in tasks_list:
        task_response.append(task.to_dict())
            
    return task_response, 200


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(include_goal_id=task.goal_id is not None), 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    print("Slack token loaded:", bool(slack_token))

    if slack_token:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {slack_token}"
            },
            json={
                "channel": "task-notifications-c26",
                "text": f"Someone just completed the task {task.title}"
            },
            timeout=10
        )

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

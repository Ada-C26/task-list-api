import os
from datetime import UTC, datetime

import requests
from flask import Blueprint, Response, request

from app.db import db
from app.models.task import Task
from app.routes.route_utilities import create_model, validate_model

SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_CHANNEL = "task-notifications-c26"
SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def call_slack_api(task):
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}

    data = {
        "channel": SLACK_CHANNEL,
        "text": f"Someone just completed the task {task.title}",
    }

    requests.post(SLACK_URL, headers=headers, json=data)


@bp.post("")
def create_task():
    data = request.get_json(silent=True)

    if (
        not isinstance(data, dict)
        or not data.get("title")
        or not data.get("description")
    ):
        return {"details": "Invalid data"}, 400

    return create_model(Task, data)


@bp.get("")
def get_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query).all()

    return [task.to_dict() for task in tasks]


@bp.get("/<int:task_id>")
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return Response(status=404)

    return task.to_dict()


@bp.put("/<int:task_id>")
@bp.put("/<int:task_id>")
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return Response(status=404)

    data = request.get_json(silent=True)

    if (
        not isinstance(data, dict)
        or not data.get("title")
        or not data.get("description")
    ):
        return {"details": "Invalid data"}, 400

    task.title = data["title"]
    task.description = data["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return Response(status=404)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(UTC)
    db.session.commit()

    call_slack_api(task)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

from flask import Blueprint, request, Response
from ..db import db
from ..models.task import Task
from .route_utilities import validate_model, create_model, send_slack_message
from datetime import datetime

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

'''Wave 1 CRUD Routes'''

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

'''Wave 2 Update get_all_tasks'''
# @bp.get("")
# def get_all_tasks():
#     query = db.select(Task).order_by(Task.id)
#     tasks = db.session.scalars(query)
#     return [task.to_dict() for task in tasks]
@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)
    return [task.to_dict() for task in tasks]

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

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


'''Wave 3 Custom Endpoints'''

@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    '''Wave 4 slack complete'''
    send_slack_message(f"Someone just completed the task {task.title}")

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

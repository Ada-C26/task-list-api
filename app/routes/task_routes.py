from ast import If
from flask import Blueprint
from flask import Response
from app.models.task import Task
from ..db import db
from flask import request
from datetime import datetime, timezone
import os
import requests
from .route_utilities import call_slack_api, get_model_by_sorting, validate_model, create_model, validate_task_model

bp = Blueprint("task_bp", __name__)

#route helper method to retrieve model by id, returns None if not found
def get_task_by_id(task_id):
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    return task

@bp.get("/tasks") # Handles GET requests to /tasks
def get_all_tasks():

    sort_param = request.args.get("sort")
    return get_model_by_sorting(Task, sort_param), 200 #helper function

@bp.get("/tasks/<int:task_id>") #dynamic URL parameter.
def get_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.post("/tasks") # Handles POST requests to /tasks
def create_task():
    request_body = request.get_json(silent=True)

    return create_model(Task, request_body)
    
@bp.put("/tasks/<int:task_id>") # Handles PUT requests to /tasks/<task_id>
def update_task(task_id):
    task = validate_model(Task, task_id)

    task_data = request.get_json() 
    title, description = validate_task_model(task_data)

    task.title = title
    task.description = description

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/tasks/<int:task_id>") # Handles DELETE requests to /tasks/<task_id>
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


#wave 3
@bp.patch("/tasks/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()
    call_slack_api(task)
    return Response(status=204, mimetype="application/json")

@bp.patch("/tasks/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    #this makes is_complete return False when to_dict() is called
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

 
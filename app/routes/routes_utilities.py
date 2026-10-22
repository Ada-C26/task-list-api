from ..db import db
from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal

def validate_model(model, model_id):
    try:
        model_id = int(model_id)
    except(ValueError, TypeError):
        response = {"message": f"Invalid {model.__name__} ID"}
        abort(make_response(response, 400))

    instance = db.session.get(model, model_id)

    if instance is None:
        response = {"message": f"{model.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return instance

def create_model(model, request_body):
    if not isinstance(request_body, dict):
        abort(make_response({"details":"Invalid data"}, 400))

    required_fields = ["title"]

    if model.__name__ == "Task":
        required_fields.append("description")

    if any(field not in request_body for field in required_fields):
        abort(make_response({"details": "Invalid data"}, 400))
              
    new_instance = model.from_dict(request_body)
    db.session.add(new_instance)
    db.session.commit()
    return new_instance.to_dict(), 201

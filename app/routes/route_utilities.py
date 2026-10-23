from flask import abort, make_response
from ..db import db
import requests
import os


def create_model(cls, model_data):
    try:
        model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(model)
    db.session.commit()

    return model.to_dict(), 201


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        sort_by = filters.get("sort_by", "title")  # sort by title by default

        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.where(getattr(cls, key).ilike(f"%{value}%"))
            elif key == "sort" and value == "asc":
                query = query.order_by(getattr(cls, sort_by).asc())
            elif key == "sort" and value == "desc":
                query = query.order_by(getattr(cls, sort_by).desc())

    models = db.session.scalars(query)
    response = [model.to_dict() for model in models]

    return response


def send_message(title):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"authorization": os.environ.get("SLACK_TOKEN")}
    message = {
        "channel": "task-notifications-c26",
        "text": f"Someone just completed the task {title}",
    }

    response = requests.post(url, json=message, headers=headers)
    return response.json()

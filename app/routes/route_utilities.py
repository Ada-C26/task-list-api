import os

from flask import abort, make_response
import requests
from app.db import db

#validate
#works for task and goal models 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        abort(make_response({"details": f"{cls.__name__} {model_id} invalid"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"details": f"{cls.__name__} {model_id} not found"}, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except (KeyError, TypeError):
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_model_by_sorting(model, sort_param):
    query = db.select(model)

    if sort_param == "asc":
        query = query.order_by(model.title.asc())
    elif sort_param == "desc":
        query = query.order_by(model.title.desc())
    else:
        query = query.order_by(model.id)

    models = db.session.scalars(query).all()

    return [item.to_dict() for item in models]

def validate_task_model(task_data):
    try: 
        title = task_data["title"]
        description = task_data["description"]
    except (KeyError, TypeError):
        abort(make_response({"details": "Invalid data"}, 400))

    return title, description

def call_slack_api(task):
    #wave 4: 
    SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

    # Send notification
    if SLACK_TOKEN and SLACK_CHANNEL:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_TOKEN}"
            },
            json={
                "channel": SLACK_CHANNEL,
                "text": f"Someone just completed the task {task.title}"
            },
            # timeout=10
        )

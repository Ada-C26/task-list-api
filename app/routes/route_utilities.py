from flask import abort, make_response
from app.db import db
import os
import requests


def validate_model(cls, id):
    try:
        id = int(id)
    except (ValueError, TypeError):
        abort(make_response({"message": f"{cls.__name__} {id} invalid"}, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return model


def create_model(cls, data):
    if not isinstance(data, dict):
        abort(make_response({"details": "Invalid data"}, 400))

    try:
        model = cls.from_dict(data)
    except (KeyError, ValueError):
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(model)
    db.session.commit()

    return model


def get_models_with_sort_response(cls, params):
    sort = params.get("sort")
    query = db.select(cls)

    if sort == "asc":
        query = query.order_by(cls.title.asc())
    elif sort == "desc":
        query = query.order_by(cls.title.desc())

    models = db.session.scalars(query).all()

    return [model.to_dict() for model in models]


def get_models_with_filters_with_response(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]


def call_slack_api(task):
    return requests.post(
        os.getenv("SLACK_URL"),
        headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"},
        json={
            "channel": os.getenv("SLACK_CHANNEL"),
            "text": f"Someone just completed the task {task.title}!",
        },
        timeout=10,
    )

import os
import math
import requests
from flask import abort, make_response, Response
from sqlalchemy import asc, desc, String, Integer, Float, Boolean, DateTime
from ..db import db
from datetime import datetime
from sqlalchemy import inspect

def quiet_success_response():
    return Response(status=204, mimetype="application/json")

def validate_model(model, model_id):
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        response = {"details": "Invalid data"}
        abort(make_response(
            response,
            # {"message": f"{model.__name__.lower()} {model_id} invalid"},
            400
        ))

    instance = db.session.get(model, model_id)

    if instance is None:
        abort(make_response(
            {"message": f"{model.__name__.lower()} {model_id} not found"},
            404
        ))

    return instance

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        # response = {"message": f"Invalid request: missing {error.args[0]}"}
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def update_model(model, updated_data):
    attributes = [attr.key for attr in inspect(model.__class__).mapper.column_attrs]

    model_mapper = inspect(model.__class__)
    
    for attr in attributes:
        if attr in updated_data and attr != "id":
            column = model_mapper.columns[attr]
            value = updated_data[attr]

            try:
                if value is None:
                    if column.nullable:
                        setattr(model, attr, None)
                        continue
                    raise ValueError

                if isinstance(column.type, String):
                    if not isinstance(value, str):
                        raise ValueError
                    data = str(value)

                elif isinstance(column.type, Integer):
                    data = int(value)

                elif isinstance(column.type, Float):
                    data = float(value)

                elif isinstance(column.type, Boolean):
                    if not isinstance(value, bool):
                        raise ValueError
                    data = bool(value)
                    
                elif isinstance(column.type, DateTime):
                    if isinstance(value, str):
                        data = datetime.fromisoformat(value)
                    elif isinstance(value, datetime):
                        data = value
                    else:
                        raise ValueError

                else:
                    raise ValueError

                setattr(model, attr, data)
            except ValueError:
                response = {"message": f"Invalid request: datatype mismatch for {attr}"}
                # response = {"details": "Invalid data"}
                abort(make_response(response, 400))

    db.session.commit()
    return quiet_success_response()

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters and isinstance(filters, dict):
        for column, value in filters.items():
            if column == "sort":
                if value == "asc":
                    query = query.order_by(asc(cls.sort_column()))
                elif value == "desc":
                    query = query.order_by(desc(cls.sort_column()))
            
            elif hasattr(cls, column):
                query = query.where(getattr(cls, column).ilike(f"%{value}%"))

    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]

    return models_response

def send_slack_notification(channel, message):
    endpoint = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACKBOT_TOKEN", "")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    request_data = {
        "channel": channel,
        "text": message
    }

    response = requests.post(endpoint, json=request_data, headers=headers)

    return response
from flask import abort, make_response, jsonify
from .db import db

def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        abort(400)

    query = db.select(model_class).where(model_class.id == model_id)
    model = db.session.scalar(query)

    if model is None:
        response = {
            "message": f"{model_class.__name__.lower()} {model_id} not found"
        }
        abort(make_response(response, 404))

    return model

def create_model_with_response(model_class, request_body):
    try:
        new_model = model_class.from_dict(request_body)
    except (KeyError, TypeError):
        response = jsonify({"details": "Invalid data"})
        response.status_code = 400
        abort(response)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters_with_response(model_class, query_params):
    query = db.select(model_class)

    sort = query_params.get("sort")

    if model_class.__name__ == "Task" and sort == "asc":
        query = query.order_by(model_class.title.asc())
    elif model_class.__name__ == "Task" and sort == "desc":
        query = query.order_by(model_class.title.desc())
    else:
        query = query.order_by(model_class.id)

    models = db.session.scalars(query)

    models_response = []

    for model in models:
        models_response.append(model.to_dict())

    return models_response, 200

create_model = create_model_with_response
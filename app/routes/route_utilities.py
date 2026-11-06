from flask import abort, make_response

from app.db import db


def validate_model(model, model_id):
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        abort(
            make_response(
                {"details": "Invalid ID"},
                400,
            )
        )

    instance = db.session.get(model, model_id)

    if instance is None:
        abort(
            make_response(
                {"message": "Not found"},
                404,
            )
        )

    return instance


def create_model(model, request_body):
    try:
        new_model = model.from_dict(request_body)
    except (KeyError, TypeError):
        abort(
            make_response(
                {"details": "Invalid data"},
                400,
            )
        )

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

from flask import abort, jsonify, make_response
from ..db import db


def validate_model(model, model_id):
    # Check that the ID is a number.
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        response = make_response(
            jsonify({"details": "Invalid ID"}),
            400
        )
        abort(response)

    # Find the record in the database.
    record = db.session.get(model, model_id)

    # Return an error if the record does not exist.
    if record is None:
        response = make_response(
            jsonify({"details": f"{model.__name__} not found"}),
            404
        )
        abort(response)

    return record


def create_model(model, model_data):
    # Check which fields are required.
    if model.__name__ == "Task":
        required_fields = ["title", "description"]
    else:
        required_fields = ["title"]

    # Check that the data has all required fields.
    if not isinstance(model_data, dict) or not all(
        field in model_data for field in required_fields
    ):
        response = make_response(
            jsonify({"details": "Invalid data"}),
            400
        )
        abort(response)

    # Create and save the new model.
    new_model = model.from_dict(model_data)
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201
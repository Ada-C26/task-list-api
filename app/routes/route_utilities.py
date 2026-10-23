from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):                                                      # cls is the model pasted in
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{clas.__name__} {model_id} invalid"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {Model_id} not found"}, 404))  # cls.__name__ turns it into the text "Task" for the error message
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))                          # stops the request immediately and sends that error response

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

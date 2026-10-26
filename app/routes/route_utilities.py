from flask import abort, make_response, Response
from ..db import db
from sqlalchemy import inspect

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, data):
    try:
        new_model = cls.from_dict(data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()
    
    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        sort_by = filters.get("sort_by")
        sort_order = filters.get("sort_order")

        for key, value in filters.items():
            if key in ["sort_by", "sort_order"]:
                continue
            if hasattr(cls, key):
                query = query.where(getattr(cls, key).ilike(f"%{value}%"))

        if sort_by and hasattr(cls, sort_by):
            sort_column = getattr(cls, sort_by)
            if sort_order.lower() == "asc":
                query = query.order_by(sort_column.asc())
            elif sort_order.lower() == "desc":
                query = query.order_by(sort_column.desc())
    
    models = db.session.scalars(query).all()
    return [model.to_dict() for model in models]

def update_model(cls, model_id, model_data):
    model = validate_model(cls, model_id)

    mapper = inspect(cls)

    for key, value in model_data.items():
        if key in mapper.columns:
            column = mapper.columns[key]

            try:
                expected_type = column.type.python_type
            except NotImplementedError:
                expected_type = None
            
            if expected_type and not isinstance(value, expected_type) and value is not None:
                continue
            
            setattr(model, key, value)
    
    db.session.commit()
    return Response(status=204, mimetype='application/json')

def delete_model(cls, model_id):
    model = validate_model(cls, model_id)
    db.session.delete(model)
    db.session.commit()
    return Response(status=204, mimetype='application/json')
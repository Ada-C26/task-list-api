from flask import Blueprint, request
from ..models.task import Task
from .route_utilities import create_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/taks")        # @bp.post handles POST /tasks

@bp.post("")
def create_task():                                              # the helpers will do the work
    request_body = request.get_json()
    return create_model(Task, request_body)

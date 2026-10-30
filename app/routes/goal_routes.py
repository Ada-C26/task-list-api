from flask import Blueprint, request, Response
from ..db import db
from ..models.goal import Goal
from .route_utilities import validate_model, create_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

'''Wave 5 CRUD Routes'''

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)
    return [goal.to_dict() for goal in goals]


@bp.get("/<goal_id>")
def get_one_task(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# '''Wave 3 Custom Endpoints'''

# @bp.patch("/<task_id>/mark_complete")
# def mark_task_complete(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now()
#     db.session.commit()

#     '''Wave 4 slack complete'''
#     send_slack_message(f"Someone just completed the task {task.title}")

#     return Response(status=204, mimetype="application/json")


# @bp.patch("/<task_id>/mark_incomplete")
# def mark_task_incomplete(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = None
#     db.session.commit()

#     return Response(status=204, mimetype="application/json")

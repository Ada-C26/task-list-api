from flask import Blueprint, Response, request
from app.models.goal import Goal
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model, create_model

bp = Blueprint("goal_bp", __name__)

# GET 
@bp.get("/goals") #execute get_all_goals() whenever someone sends a GET request to /goals.
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query).all()

    return [goal.to_dict() for goal in goals], 200

# GET /goals/<goal_id>
@bp.get("/goals/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200

# POST /goals
@bp.post("/goals")
def create_goal():
    request_body = request.get_json(silent=True)

    return create_model(Goal, request_body)

@bp.put("/goals/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    goal.title = request_body["title"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# DELETE 
@bp.delete("/goals/<int:goal_id>")
def delete_goal(goal_id):
    # Find the goal by its ID
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# POST
@bp.post("/goals/<int:goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    #list comprehension to validate each task ID and retrieve the corresponding Task objects
    goal.tasks = [validate_model(Task, task_id) for task_id in task_ids]
    db.session.commit()
    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }, 200

# GET /goals/<goal_id>/tasks
@bp.get("/goals/<int:goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict, 200

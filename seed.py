from dotenv import load_dotenv

from app import create_app, db
from app.models.goal import Goal
from app.models.task import Task


goals = [
    {
        "title": "Build a habit of going outside daily",
        "tasks": [
            {
                "title": "Go on my daily walk",
                "description": "Notice something new every day",
                "completed_at": None,
            },
            {
                "title": "Water the garden",
                "description": "Keep the plants healthy",
                "completed_at": None,
            },
            {
                "title": "Take a short hike",
                "description": "Explore a nearby trail",
                "completed_at": None,
            },
        ],
    },
    {
        "title": "Stay on top of responsibilities",
        "tasks": [
            {
                "title": "Answer forgotten email",
                "description": "Reply emails asap",
                "completed_at": None,
            },
            {
                "title": "Pay my bills",
                "description": "Check deadlines and make payments",
                "completed_at": None,
            },
        ],
    },
    {
        "title": "Improve my daily routine",
        "tasks": [
            {
                "title": "Make the bed",
                "description": "Maybe change the bedsheet.",
                "completed_at": None,
            },
            {
                "title": "Read for 20 minutes",
                "description": "Read a book before bed",
                "completed_at": None,
            },
        ],
    },
]

standalone_tasks = [
    {
        "title": "Organize my desk",
        "description": "Clear unnecessary clutter",
        "completed_at": None,
    },
    {
        "title": "Clean out my inbox",
        "description": "Delete unnecessary emails",
        "completed_at": None,
    },
]


def get_model_by_field(cls, data_dict, key_name):
    value = data_dict[key_name]
    stmt = db.select(cls).where(getattr(cls, key_name) == value)
    return db.session.scalar(stmt)


load_dotenv()

my_app = create_app()

with my_app.app_context():
    for goal_data in goals:
        goal = get_model_by_field(Goal, goal_data, "title")

        if not goal:
            goal = Goal(title=goal_data["title"])
            db.session.add(goal)
            db.session.flush()

        for task_data in goal_data["tasks"]:
            task = get_model_by_field(Task, task_data, "title")

            if not task:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    completed_at=task_data["completed_at"],
                    goal_id=goal.id,
                )
                db.session.add(task)

    # Add standalone tasks (without a goal)
    for task_data in standalone_tasks:
        task = get_model_by_field(Task, task_data, "title")

        if not task:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                completed_at=task_data["completed_at"],
                goal_id=None,
            )
            db.session.add(task)

    db.session.commit()

    print("Database seeded successfully!")
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Task(db.Model):
    # The database creates a unique ID for each task.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # These fields store the task title and description.
    title: Mapped[str] = mapped_column(db.Text, nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)

    # This field stores when the task was completed.
    # None means the task is not complete.
    completed_at: Mapped[datetime | None] = mapped_column(
        db.DateTime,
        nullable=True
    )

    def to_dict(self):
        # Convert the task object into a dictionary for the API.
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

    @classmethod
    def from_dict(cls, task_dict):
        # Create a new Task object from a dictionary.
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=None
        )

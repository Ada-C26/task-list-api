from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Task(db.Model):
    # The database creates a unique ID for each task.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

        # This stores the ID of the goal.
    # None means the task has no goal.
    goal_id: Mapped[Optional[int]] = mapped_column(
        db.ForeignKey("goal.id"),
        nullable=True
    )

    # This gives access to the Goal object.
    goal: Mapped[Optional["Goal"]] = relationship(
        back_populates="tasks"
    )

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
            "goal_id": self.goal_id,
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

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]

    completed_at: Mapped[datetime | None]

    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goal.id"))

    goal: Mapped["Goal | None"] = relationship(
        back_populates="tasks"
    )

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"]
        )

        return new_task
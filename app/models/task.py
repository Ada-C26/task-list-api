from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(default=None)
    is_complete = False
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["title"] = self.title
        result["description"] = self.description
        result["is_complete"] = True if self.completed_at else False

        if self.goal_id:
            result["goal_id"] = self.goal_id

        return result

    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")

        task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at"),
            is_complete=True if task_data.get("completed_at") else False,
            goal_id=goal_id,
        )
        return task

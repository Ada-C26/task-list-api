from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime, timezone
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")



    def to_dict(self):
        task_as_dict = {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : self.is_complete
        }

        if self.goal:
            task_as_dict["goal_id"] = self.goal.id
        
        return task_as_dict
    
    @property
    def is_complete(self):
        return self.completed_at is not None

    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")

        new_task = cls(title=task_data["title"], description=task_data["description"], completed_at=task_data.get("completed_at"), goal_id=goal_id)

        return new_task

    def mark_complete(self):
        self.completed_at = datetime.now(timezone.utc)
    
    def mark_incomplete(self):
        self.completed_at = None


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    #check if the instance has a goal and only then set the id.
    def to_dict(self):
        task_dict =  {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal is not None:
            task_dict["goal_id"] = self.goal.id
        return task_dict
    

    #@classmethod allows the method to work with the Task class itself.
    #cls represents the class (Task).
    @classmethod
    def from_dict(cls, task_data):
        return cls( #creates and returns a new Task instance.
            title=task_data["title"], #retrieves the title from the incoming dictionary.
            description=task_data["description"],
            completed_at=None
        )



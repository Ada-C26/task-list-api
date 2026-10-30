from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]                    # makes column nullable

    # Model Helper Methods

    ##Task object -> Python dict
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None        # gives False when there's no date

        }

    #Python dict <- from_dict() <- Task object
    @classmethod                                                #classmethod to accept a dict, create new Task instance
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],                           # raises KeyError if key is missing
            description=task_data["description"],
            completed_at=None
        )



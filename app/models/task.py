from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["is_complete"] = self.completed_at is not None
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict

    @classmethod
    def from_dict(cls, data):
        goal_id = data.get("goal_id")

        return cls(
            title=data["title"],
            description=data["description"],
            completed_at=datetime.fromisoformat(data["completed_at"]) if isinstance(data.get("completed_at"), datetime) else None,
            goal_id=goal_id
        )
    
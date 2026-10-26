from asyncio import tasks
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[Optional[list["Task"]]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] = self.id
        goal_dict["title"] = self.title

        if self.tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]
        
        return goal_dict
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"]
        )
    
    

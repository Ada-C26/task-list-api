from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING

'''Wave 6 connect tasks with goals'''
if TYPE_CHECKING:
    from .task import Task

'''Wave 5 Goal Model'''

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    #Wave 6
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title":self.title
        }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])

from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, goal_data):
        title = goal_data["title"]

        if not title:
            raise ValueError("Invalid title")

        return cls(title=title)

    def to_dict(self):
        return {"id": self.id, "title": self.title}

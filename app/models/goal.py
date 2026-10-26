from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    # has many Task relationship
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal") # noqa: F821

    def to_dict(self):
        dictionary = {
            "id": self.id or None,
            "title": self.title or None
        }

        return dictionary

    @classmethod
    def from_dict(cls, record_data: dict):
        return cls(
            title=record_data["title"]
        )
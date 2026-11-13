
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Goal(db.Model):
    # The database creates a unique ID for each goal.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # This field stores the goal title.
    title: Mapped[str] = mapped_column(db.Text, nullable=False)

    # This gives access to the tasks associated with the goal.
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="goal"
    )

    def to_dict(self):
        # Convert the Goal object into a dictionary.
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, goal_dict):
        # Create a new Goal object from a dictionary.
        return cls(
            title=goal_dict["title"]
        )


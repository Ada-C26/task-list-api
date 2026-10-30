from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

'''Wave1 Create Task Model'''
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]                                    #Wave 3, is_complete returns true or flase

    '''Wave1 Model Helper Methods'''

    #Task object -> Python dict
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None

        }

    #Python dict <- from_dict() <- Task object
    @classmethod
    def from_dict(cls, task_data):#
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=None
        )

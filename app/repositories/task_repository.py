from ..models.task import Task
from .base_repository import BaseRepository
from ..db import db
from datetime import datetime

class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(db, Task)

    def validate(self, record_data: dict):
        try:
            title = record_data["title"]
            description = record_data.get("description", "")
            completed_at = record_data.get("completed_at", None)
        except KeyError:
            return False

        if completed_at is not None and not isinstance(completed_at, datetime):
            return False

        return {
            "title": title,
            "description": description,
            "completed_at": completed_at,
        }
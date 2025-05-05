from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
from enum import Enum
from typing import Optional


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoBase(BaseModel):
    id: int
    title: str
    priority: PriorityEnum = PriorityEnum.medium
    is_done: bool
    created_at: datetime
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    is_done: bool


class Todo(TodoBase):
    @field_serializer("created_at")
    def format_created_at(self, created_at: datetime) -> str:
        return created_at.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("due_date")
    def format_due_date(self, due_date: Optional[datetime]) -> str:
        return due_date.strftime("%Y-%m-%d %H:%M:%S") if due_date else "Not set"
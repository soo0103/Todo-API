from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
from database import Base
from datetime import datetime
from schemas import PriorityEnum


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(SqlEnum(PriorityEnum), default=PriorityEnum.medium)
    due_date = Column(DateTime, nullable=True)
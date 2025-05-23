from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from app.db.db_session import engine
from enum import Enum
from datetime import datetime


class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Event(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    start_time: datetime 
    end_time: datetime 
    location: Optional[str] 
    is_recurring: bool
    recurrence_pattern: Optional[RecurrencePattern] 
    owner_id: int = Field(foreign_key="user.id")
    create_dtm: Optional[datetime] = Field(default_factory=datetime.now)

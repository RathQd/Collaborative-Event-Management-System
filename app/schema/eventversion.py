from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ReadEventVersion(BaseModel):
    id: int
    event_id: int
    version_id: UUID
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    is_recurring: bool
    recurrence_pattern: Optional[str]
    edited_by: int
    edited_at: datetime

    class Config:
        from_attributes = True


class CreateEventVersion(BaseModel):
    event_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    edited_by: int

    class Config:
        from_attributes = True

from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

class EventVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int
    version_id: UUID = Field(default_factory=uuid4, index=True, unique=True)
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    is_recurring: bool
    recurrence_pattern: Optional[str]
    owner_id: int 
    edited_by: int = Field(foreign_key="user.id")
    edited_at: datetime = Field(default_factory=datetime.now)    
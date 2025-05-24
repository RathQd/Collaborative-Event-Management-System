from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional

class PermissionLevel(str, Enum):
    owner = "owner"
    editor = "editor"
    view = "viewer"

class EventPermission(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    user_id: int = Field(foreign_key="user.id")
    permission: PermissionLevel
    event: Optional["Event"] = Relationship(back_populates="permissions")

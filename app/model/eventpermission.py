from sqlmodel import SQLModel, Field
from enum import Enum

class PermissionLevel(str, Enum):
    owner = "owner"
    editor = "editor"
    view = "viewer"

class EventPermission(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    user_id: int = Field(foreign_key="user.id")
    permission: PermissionLevel


# class EventPermission(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     event_id: int = Field(foreign_key="event.id")
#     user_id: int = Field(foreign_key="user.id")
#     permission: PermissionLevel

#     __table_args__ = (
#         UniqueConstraint("event_id", "user_id", name="unique_event_user_permission"),
#     )
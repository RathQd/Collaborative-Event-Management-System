from pydantic import BaseModel
from typing import List
from enum import Enum

class PermissionLevel(str, Enum):
    owner = "owner"
    editor = "editor"
    view = "viewer"

class UserPermissionInput(BaseModel):
    user_id: int
    role: PermissionLevel

class ShareEventRequest(BaseModel):
    users: List[UserPermissionInput]

class PermissionInfo(BaseModel):
    user_id: int
    permission: PermissionLevel

class UpdatePermissionRequest(BaseModel):    
    permission: PermissionLevel


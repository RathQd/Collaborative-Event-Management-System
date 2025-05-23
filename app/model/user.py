from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from app.db.db_session import engine
from typing import Optional
import datetime

class User(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    # username: str = Field(default=None, primary_key=True)
    username: str 
    email: EmailStr 
    # email: EmailStr = Field(index=True, unique=True)
    password_hashed: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)





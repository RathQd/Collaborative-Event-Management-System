from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Event(BaseModel):        
    title: str 
    description: str 
    start_time: datetime 
    end_time: datetime 
    location: Optional[str] 
    is_recurring: bool  
    recurrence_pattern: Optional[RecurrencePattern]     

class ReadEvent(BaseModel):     
    title: str 
    description: str 
    start_time: datetime 
    end_time: datetime 
    location: Optional[str] 
    is_recurring: bool  
    owner_id: int
    recurrence_pattern: Optional[RecurrencePattern]         

class ReadEvent(BaseModel):     
    title: str 
    description: str 
    start_time: datetime 
    end_time: datetime 
    location: Optional[str] 
    is_recurring: bool  
    owner_id: int
    recurrence_pattern: Optional[RecurrencePattern]   

class ReadListEvent(BaseModel):     
    id: int
    title: str 
    description: str 
    start_time: datetime 
    end_time: datetime 
    location: Optional[str] 
    is_recurring: bool  
    owner_id: int
    recurrence_pattern: Optional[RecurrencePattern]  
from app.model.eventversion import EventVersion
from uuid import UUID
from sqlmodel import select
from typing import List

async def get_logs_by_event_id(event_id, session)->List[EventVersion]:        
        query = select(EventVersion).where(EventVersion.event_id == event_id).order_by(EventVersion.edited_at.desc())
        result = session.exec(query).all()
        return result
from fastapi import HTTPException, status
from app.model.eventversion import EventVersion
from uuid import UUID
from sqlmodel import select

async def get_event_version_by_uuid(id:UUID, event_id, session)->EventVersion:        
        try:                
            query = select(EventVersion).where(EventVersion.version_id == id, EventVersion.event_id == event_id)
            result = session.exec(query).first()
            return result
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get_event_version_by_uuid : {str(e)}"
            ) 
        
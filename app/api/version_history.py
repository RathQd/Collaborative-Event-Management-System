from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from app.db.db_session import get_session
from app.services.auth_service import get_current_user
from app.model.eventversion import EventVersion
from app.model.event import Event, RecurrencePattern
from app.schema.token import TokenUserData
from uuid import UUID
from app.crud.version_history import get_event_version_by_uuid
from app.crud.collaboration import is_collaborator
from app.crud.event import update_event_by_id


router = APIRouter()

# GET /api/events/{id}/history/{versionId} - Get a specific version of an event

@router.get("/{id}/history/{version_id}", status_code=status.HTTP_200_OK,response_model=EventVersion)
async def get_event_version(id: int, version_id: UUID, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    print(version_id)
    version = await get_event_version_by_uuid(version_id, id, session)    
    if not version:
        raise HTTPException(status_code=404, detail="Event version not found")
    has_access = (
            version.owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to retrieve event version")
    return version
    


# POST /api/events/{id}/rollback/{versionId} - Rollback to a previous version

@router.post("/{id}/rollback/{version_id}", status_code=status.HTTP_200_OK)
async def rollback_event(id: int, version_id: UUID, current_user:TokenUserData=Depends(get_current_user), session: Session = Depends(get_session)):
    version = await get_event_version_by_uuid(version_id, id, session)    
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    has_access = (
            version.owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to rollback event version")
    event = Event(id=id, 
                  title=version.title, 
                  description=version.description, 
                  start_time=version.start_time,
                  end_time=version.end_time,
                  location=version.location,
                  is_recurring=version.is_recurring,
                  recurrence_pattern=RecurrencePattern[version.recurrence_pattern.split('.')[-1]])
    updated_event = await update_event_by_id(id=id, event=event, user_id=current_user.id, session=session)    
    return {"detail": f"Event rolled back to version {version_id}", "event": updated_event}
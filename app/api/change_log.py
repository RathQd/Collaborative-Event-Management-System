from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from app.db.db_session import get_session
from app.services.auth_service import get_current_user
from app.model.eventversion import EventVersion
from app.schema.token import TokenUserData
from app.crud.change_log import get_logs_by_event_id
from app.crud.collaboration import is_collaborator
from app.crud.version_history import get_event_version_by_uuid
from typing import List, Any
from uuid import UUID
from app.utils.compare_version import compare_event_versions
from fastapi_cache.decorator import cache


router = APIRouter()

# GET /api/events/{id}/changelog - Get a chronological log of all changes to an event

@router.get("/{id}/changelog", status_code=status.HTTP_200_OK,response_model=List[EventVersion])
@cache(expire=120)
async def get_event_change_logs(id: int, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    logs = await get_logs_by_event_id(id, session)    
    if not logs:
        raise HTTPException(status_code=404, detail="Changelogs are not available")
    has_access = (
            logs[0].owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to view changelog")
    return logs

# GET /api/events/{id}/diff/{versionId1}/{versionId2} - Get a diff between two versions

@router.get("/{id}/diff/{versionId1}/{versionId2}", status_code=status.HTTP_200_OK,response_model=dict[str, dict[str, Any]])
@cache(expire=120)
async def diff_versions(id: int, versionId1: UUID, versionId2: UUID, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    version1 = await get_event_version_by_uuid(id=versionId1, event_id=id, session=session)    
    version2 = await get_event_version_by_uuid(id=versionId2, event_id=id, session=session)    
    
    if not version1:
        raise HTTPException(status_code=404, detail=f"Event version not found with {versionId1}")
    if not version2:
        raise HTTPException(status_code=404, detail=f"Event version not found with {versionId2}")
    has_access = (
            version1.owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to view difference of versions")
    
    version_difference = await compare_event_versions(version1=version1, version2=version2)

    return version_difference
    
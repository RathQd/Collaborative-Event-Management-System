from fastapi import APIRouter, status, Depends, HTTPException, status
from app.schema.permission import PermissionInfo, ShareEventRequest, UpdatePermissionRequest
from app.schema.token import TokenUserData
from typing import List
from copy import deepcopy
from app.services.auth_service import get_current_user
from app.db.db_session import get_session
from app.crud.event import get_event_by_id
from app.crud.collaboration import check_existing_permission, insert_event_permissions, is_collaborator, list_event_permissions, update_event_permission, delete_event_permission

from sqlmodel import Session

router = APIRouter()

@router.post("/{id}/share", response_model=ShareEventRequest, status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Bad request"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def share_event(id: int, share_event_req: ShareEventRequest, session: Session = Depends(get_session), current_user: TokenUserData = Depends(get_current_user)):
    updated_events = deepcopy(share_event_req)
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="permission denied ! You need to be a owner of the event to share")
        
    event_req_to_insert = await check_existing_permission(share_event_req=share_event_req, event_id=id, session=session)    
    await insert_event_permissions(event_req_to_insert=event_req_to_insert, event_id=id, session=session)
    return updated_events

@router.get("/{id}/permissions", response_model=List[PermissionInfo], status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def list_permissions(id: int, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not event or (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="permission denied")
    permissions = await list_event_permissions(event_id=id, session=session)            
    return permissions


@router.put("/{id}/permissions/{user_id}", response_model=PermissionInfo, status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def update_permission(id: int, user_id: int, permission_req: UpdatePermissionRequest, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not event or (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="permission denied")

    updated_permission = await update_event_permission(event_id=id, user_id=user_id, permission_to_update=permission_req, session=session)
    return updated_permission


@router.delete("/{id}/permissions/{user_id}", response_model=PermissionInfo, status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def delete_permission(id: int, user_id: int, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not event or (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="permission denied")

    updated_permission = await delete_event_permission(event_id=id, user_id=user_id, session=session)
    return updated_permission



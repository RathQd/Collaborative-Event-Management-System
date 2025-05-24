from fastapi import APIRouter, status, Depends, HTTPException, status
from app.schema.permission import PermissionInfo, ShareEventRequest, UpdatePermissionRequest
from app.schema.token import TokenUserData
from typing import List
from copy import deepcopy
from app.services.auth_service import get_current_user
from app.db.db_session import get_session
from app.crud.event import get_event_by_id
from app.crud.user import get_user_by_id
from app.crud.collaboration import check_existing_permission, insert_event_permissions_batch, is_collaborator, list_event_permissions, update_event_permission, delete_event_permission
from sqlmodel import Session
from fastapi_cache.decorator import cache

router = APIRouter()

# POST /api/events/{id}/share - Share an event with other users

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
        raise HTTPException(status_code=404, detail="Event with id={id} not found")
    if (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="Permission denied ! You need to be a owner of the event to share")
    
    for user_reqs in share_event_req.users:                    
            await get_user_by_id(user_reqs.user_id, session)
    
    event_req_to_insert = await check_existing_permission(share_event_req=share_event_req, event_id=id, session=session)    
    await insert_event_permissions_batch(event_req_to_insert=event_req_to_insert, event_id=id, session=session)
    return updated_events

# GET /api/events/{id}/permissions - List all permissions for an event

@router.get("/{id}/permissions", response_model=List[PermissionInfo], status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
@cache(expire=120)
async def list_permissions(id: int, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="Event with id={id} not found")
    if (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="Permission denied: you are not allowed to view permissions")
    permissions = await list_event_permissions(event_id=id, session=session)            
    return permissions

# PUT /api/events/{id}/permissions/{userId} - Update permissions for a user

@router.put("/{id}/permissions/{user_id}", response_model=PermissionInfo, status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def update_permission(id: int, user_id: int, permission_req: UpdatePermissionRequest, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="Event with id={id} not found")
    if (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="Permission denied: you are not allowed to update permissions")

    updated_permission = await update_event_permission(event_id=id, user_id=user_id, permission_to_update=permission_req, session=session)
    return updated_permission

# DELETE /api/events/{id}/permissions/{userId} - Remove access for a user

@router.delete("/{id}/permissions/{user_id}", response_model=PermissionInfo, status_code=status.HTTP_200_OK, 
    responses={
        404: {"description": "Event not Found"},
        403: {"description": "Permission denied"},
        500: {"description": "Internal server error"}
    })
async def delete_permission(id: int, user_id: int, session: Session = Depends(get_session), current_user:TokenUserData = Depends(get_current_user)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=404, detail="Event with id={id} not found")
    if (event.owner_id != current_user.id and not await is_collaborator(event_id=id, user_id=current_user.id, session=session)):
        raise HTTPException(status_code=403, detail="Permission denied: you are not allowed to delete permissions")

    updated_permission = await delete_event_permission(event_id=id, user_id=user_id, session=session)
    return updated_permission



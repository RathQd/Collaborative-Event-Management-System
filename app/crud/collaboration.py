from typing import List
from fastapi import HTTPException, status
from app.schema.permission import ShareEventRequest, PermissionInfo, UpdatePermissionRequest
from app.model.eventpermission import EventPermission, PermissionLevel
from app.model.event import Event
from sqlmodel import select

async def check_existing_permission(share_event_req: ShareEventRequest, event_id: int, session) -> ShareEventRequest:
    try:
        user_ids = [user.user_id for user in share_event_req.users]                
        query = select(EventPermission.user_id, EventPermission.permission).where(
            EventPermission.event_id == event_id,
            EventPermission.user_id.in_(user_ids)
        )
        existing_permission = session.exec(query).all()        
        existing_map = {user_id: permission for user_id, permission in existing_permission}
        
        to_update = [
            user for user in share_event_req.users
            if existing_map.get(user.user_id) != user.role
        ]

        return ShareEventRequest(users=to_update)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking existing permissions: {str(e)}"
        )

async def insert_event_permissions_batch(event_req_to_insert: ShareEventRequest, event_id: int, session):
    try:        
        new_permissions = [
            EventPermission(
                event_id=event_id,
                user_id=user.user_id,
                permission=user.role
            )
            for user in event_req_to_insert.users
        ]
        session.add_all(new_permissions)
        session.commit()

        return {"Message": "Permissions successfully assigned"}

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assign permissions: {str(e)}"
        )


async def insert_event_permission_owner(events:List[Event], user_id: int, session):
    try:        
        permissions = [
            EventPermission(event_id=event.id, user_id=user_id, permission=PermissionLevel.owner)
            for event in events
        ]

        session.add_all(permissions)
        session.commit()

        return {"Message": "Permissions successfully assigned"}

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assign permissions: {str(e)}"
        )


async def is_collaborator(event_id: int, user_id: int, session) -> bool:
    try:
        query = select(EventPermission).where(
            EventPermission.event_id == event_id,
            EventPermission.user_id == user_id,
            EventPermission.permission == PermissionLevel.editor  
        )
        result = session.exec(query).first()
        return result is not None

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find collaboration status : {str(e)}"
        )


async def is_viewer(event_id: int, user_id: int, session) -> bool:
    try:
        query = select(EventPermission).where(
            EventPermission.event_id == event_id,
            EventPermission.user_id == user_id,
            EventPermission.permission == PermissionLevel.view  
        )
        result = session.exec(query).first()
        return result is not None

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find viewer status : {str(e)}"
        )

async def list_event_permissions(event_id: int, session) -> List[PermissionInfo]:
    try:
        
        query = select(EventPermission).where(EventPermission.event_id == event_id)
        result = session.exec(query).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event has no permissions yet")
        
        permissions = [
            PermissionInfo(user_id=record.user_id, permission=record.permission)
                for record in result
            ]
        return permissions

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find the list of event permissions : {str(e)}"
        )

async def update_event_permission(event_id: int, user_id: int, permission_to_update: UpdatePermissionRequest, session)->PermissionInfo:
    try:
        query = select(EventPermission).where(
            EventPermission.event_id == event_id,
            EventPermission.user_id == user_id
        )
        existing_permission = session.exec(query).first()

        if not existing_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found for this user and event"
            )
        
        existing_permission.permission = permission_to_update.permission

        session.commit()
        session.refresh(existing_permission)
        updated_permission = PermissionInfo(user_id=user_id, permission=existing_permission.permission)
        return updated_permission
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update_event_permission: {str(e)}"
        )
    

async def delete_event_permission(event_id: int, user_id: int, session) -> PermissionInfo:
    try:
        query = select(EventPermission).where(
            EventPermission.event_id == event_id,
            EventPermission.user_id == user_id
        )
        existing_permission = session.exec(query).first()
        if not existing_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found for this user and event"
            )
        deleted_permission_info = PermissionInfo(
            user_id=existing_permission.user_id,
            permission=existing_permission.permission
        )
        session.delete(existing_permission)
        session.commit()

        return deleted_permission_info
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete_event_permission: {str(e)}"
        )

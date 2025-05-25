from typing import List
from fastapi import HTTPException, status
from app.schema.event import ReadEvent
from app.schema.permission import ShareEventRequest, UserPermissionInput, PermissionLevel
from app.model.event import Event
from app.model.eventversion import EventVersion
from app.model.eventpermission import EventPermission
from app.crud.collaboration import insert_event_permissions_batch, insert_event_permission_owner
from sqlmodel import select
from uuid import uuid4
from datetime import datetime

async def create_event(event: Event, session)->ReadEvent:        
    try:                
        session.add(event)
        session.commit()    
    except Exception as e: 
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
    session.refresh(event)
    share_event_req = ShareEventRequest(users=[UserPermissionInput(user_id=event.owner_id, role=PermissionLevel.owner)])
    await insert_event_permissions_batch(event_req_to_insert=share_event_req, event_id=event.id, session=session)
    return event

async def get_event_by_id(id: int, session)->ReadEvent:
        try:
            event = session.get(Event, id)
            return event
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete_event_by_id : {str(e)}"
            )
        

async def get_all_event_of_current_user(user_id, limit, skip, search, session):    
    all_post = session.exec(select(Event)
    .join(EventPermission, EventPermission.event_id == Event.id)
    .where(
        EventPermission.user_id == user_id,
        Event.title.contains(search)
    )
    .limit(limit)
    .offset(skip)
    .distinct()).all()
    if not all_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no event found for user")
    return all_post

async def update_event_by_id(id: int, event: Event, user_id:int, session)->ReadEvent:    
    try:
        event_to_update = session.exec(select(Event).where(Event.id == id)).first()    
        if event_to_update:
            event_version = EventVersion(
                event_id=event_to_update.id,
                version_id=uuid4(),
                title=event_to_update.title,
                description=event_to_update.description,
                start_time=event_to_update.start_time,
                end_time=event_to_update.end_time,
                location=event_to_update.location,
                is_recurring=event_to_update.is_recurring,
                recurrence_pattern=str(event_to_update.recurrence_pattern) if event_to_update.recurrence_pattern else None,
                owner_id=event_to_update.owner_id,
                edited_by=user_id,
                edited_at=datetime.now()        
            )
            session.add(event_version)

        if event_to_update: 
            event.id = id
            event_to_update = session.merge(event)
            session.add(event_to_update)
            session.commit()
            session.refresh(event_to_update)             
        return event_to_update  
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update_event_by_id : {str(e)}"
        ) 
     

async def delete_event_by_id(id: int, session)->ReadEvent:       
    try:
        event = session.get(Event, id)
        if not event:
            return print("Delete Event by ID")   
        session.delete(event)
        session.commit()
        return event
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete_event_by_id : {str(e)}"
        )


async def create_events_batch(events: List[Event], session) -> List[Event]:
    try:
        session.add_all(events)
        session.commit()        
        for event in events:
            session.refresh(event)   
        await insert_event_permission_owner(events=events, user_id=events[0].owner_id, session=session)        
        return events
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create_events_batch : {str(e)}"
        )


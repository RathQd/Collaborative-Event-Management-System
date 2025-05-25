from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException, status, BackgroundTasks
from pydantic import EmailStr
from app.schema.token import TokenUserData
from sqlmodel import Session
from app.db.db_session import get_session
from app.crud.event import create_event, get_event_by_id, delete_event_by_id, update_event_by_id, create_events_batch, get_all_event_of_current_user
from app.services.auth_service import get_current_user
from app.schema.event import Event, ReadEvent, ReadListEvent
from app.model.event import Event as WriteEvent
from app.crud.collaboration import is_collaborator, is_viewer
from app.utils.email_utils import send_email
from fastapi_cache.decorator import cache

router = APIRouter()

# POST /api/events - Create a new event

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadEvent,
    responses={
        400: {"description": "bad request"},
        500: {"description": "internal server error"}
})
async def create_new_event(event: Event, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):    
    event = WriteEvent(**event.model_dump())
    event.owner_id = current_user.id
    created_event = await create_event(event=event, session=session)    
    return created_event

# GET /api/events - List all events the user has access to with pagination and filtering

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ReadListEvent], 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
})
@cache(expire=120)
async def get_all_event(limit: int = 5, skip: int = 0, search: Optional[str] = "", current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    events = await get_all_event_of_current_user(current_user.id, limit, skip, search, session)
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Events not found")
    has_access = (
        events[0].owner_id == current_user.id
        or await is_collaborator(event_id=events[0].id, user_id=current_user.id, session=session)
        or await is_viewer(event_id=events[0].id, user_id=current_user.id, session=session)
    )    
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to view events")
    return events


# GET /api/events/{id} - Get a specific event by ID

@router.get("/{id:int}", status_code=status.HTTP_200_OK, response_model=ReadListEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
})
@cache(expire=120)
async def get_event(id: int, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id={id} not found")
    has_access = (
        event.owner_id == current_user.id
        or await is_collaborator(event_id=id, user_id=current_user.id, session=session)
        or await is_viewer(event_id=id, user_id=current_user.id, session=session)
    )    
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to view event")
    return event

# PUT /api/events/{id} - Update an event by ID

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=ReadEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
    })
async def update_event(id: int, event: Event, email: EmailStr, background_task: BackgroundTasks, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):    
    event = WriteEvent(**event.model_dump())    
    try:
        event_to_delete = await get_event_by_id(id, session)        
        if not event_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id={id} not found")        
        has_access = (
            event_to_delete.owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
        if not has_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to update event")
        event = await update_event_by_id(id, event, email, current_user.id, session)
        background_task.add_task(send_email, subject="Event Update Notification from CEMS",  body=f"The event with id='{event.id}' and title='{event.title}' has been successfully updated.", to_email=email)        
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e}")
    return event

# DELETE /api/events/{id} - Delete an event by ID

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=ReadEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
    })
async def delete_event(id: int, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    event_to_delete = await get_event_by_id(id, session)
    if not event_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id={id} not found")    
    has_access = (
            event_to_delete.owner_id == current_user.id
            or await is_collaborator(event_id=id, user_id=current_user.id, session=session)        
        )        
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: you are not allowed to delete event")
    event = await delete_event_by_id(id, session)    
    return event


# POST /api/events/batch - Create multiple events in a single request

@router.post("/batch",status_code=status.HTTP_201_CREATED,response_model=List[ReadEvent],
    responses={
        400: {"description": "Bad request"},        
        500: {"description": "Internal server error"},
    }
)
async def register_events_in_batch(events: List[Event], current_user: TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):        
    events = [WriteEvent(**event.model_dump(), owner_id = current_user.id) for event in events]        
    created_events = await create_events_batch(events=events, session=session)
    return created_events


    
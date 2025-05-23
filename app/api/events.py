from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, status
from app.schema.token import TokenUserData
from sqlmodel import Session
from app.db.db_session import get_session
from app.crud.event import create_event, get_event_by_id, delete_event_by_id, update_event_by_id, create_events_batch
from app.services.auth_service import get_current_user
from app.schema.event import Event, ReadEvent
from app.model.event import Event as WriteEvent

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadEvent,
    responses={
        400: {"description": "bad request"},
        500: {"description": "internal server error"}
})
async def register_event(event: Event, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):    
    event = WriteEvent(**event.model_dump())
    event.owner_id = current_user.id
    created_event = await create_event(event=event, session=session)    
    return created_event

@router.get("/{id:int}", status_code=status.HTTP_200_OK, response_model=ReadEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
})
async def get_event(id: int, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    event = await get_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"event not found")
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"permission denied")
    return event


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=ReadEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
    })
async def update_event(id: int, event: Event, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):    
    event = WriteEvent(**event.model_dump())    
    try:
        event = await update_event_by_id(id, event, session)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"event {id} updated")        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")
    return event

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=ReadEvent, 
    responses={
        404: {"description": "event not found"},
        500: {"description": "internal server error"}
    })
async def delete_event(id: int, current_user:TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):
    event = await delete_event_by_id(id, session)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"event {id} deleted")    
    return event

@router.post("/batch",status_code=status.HTTP_201_CREATED,response_model=List[ReadEvent],
    responses={
        400: {"description": "Bad request"},        
        500: {"description": "Internal server error"},
    }
)
async def register_events_batch(events: List[Event], current_user: TokenUserData = Depends(get_current_user), session: Session = Depends(get_session)):    
    print(events)
    events = [WriteEvent(**event.model_dump(), owner_id = current_user.id) for event in events]        
    created_events = await create_events_batch(events=events, session=session)
    return created_events


    
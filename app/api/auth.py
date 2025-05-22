from fastapi import APIRouter, status, Depends
from app.schema.User import RegisterUser, ReadUser
from sqlmodel import Session
from app.db.db_session import get_session
from app.crud.user import create_user

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ReadUser, responses={
    400: {"description": "Bad Request"},
    500: {"description": "Internal Server Error"}
})
async def register_user(user: RegisterUser, session: Session = Depends(get_session))->ReadUser:
    created_user = await create_user(user=user, session=session)
    print("Registering the User")
    return created_user




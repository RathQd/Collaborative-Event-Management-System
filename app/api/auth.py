from fastapi import APIRouter, status, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schema.User import RegisterUser, ReadUser 
from app.schema.token import Token
from sqlmodel import Session
from app.db.db_session import get_session
from app.crud.user import create_user, get_user_by_email
from app.services.auth_service import create_jwt_token, verify_jwt_token, token_blacklist
from app.utils.hash import verify_hash

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ReadUser, responses={
    400: {"description": "Bad Request"},
    500: {"description": "Internal Server Error"}
})
async def register_user(user: RegisterUser, session: Session = Depends(get_session))->ReadUser:
    created_user = await create_user(user=user, session=session)
    print("Registering the User")
    return created_user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token, responses={
    403: {"description": "User Not Found"}    
})
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session))->Token:
    try:
        user = await get_user_by_email(user_credentials.username, session)        
    except HTTPException as e:
        raise e
    access_token = await create_jwt_token(data = {"email":user.email, "id": user.id})
    if not await verify_hash(user_credentials.password, user.password_hashed):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password or Email Id")
    read_token = Token(access_token=access_token, token_type='bearer')
    return read_token


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token, responses={
    403: {"description": "User Not Found"}    
})
async def refresh(user_token_data:Token, session: Session = Depends(get_session))->Token:    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials", headers={"WWW-Authenticate":"Bearer"})
    try:        
        user = await verify_jwt_token(token=user_token_data.access_token, credentials_exception=credentials_exception)
        token_user_data = await get_user_by_email(user.email, session)                
    except HTTPException as e:
        raise e    
    access_token = await create_jwt_token(data = {"email":token_user_data.email, "id": token_user_data.id})
    read_token = Token(access_token=access_token, token_type='bearer')
    return read_token

@router.post("/logout", status_code=status.HTTP_200_OK, responses={
    403: {"description": "User Not Found"}    
})
async def logout(user_token_data:Token, session: Session = Depends(get_session)):    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials", headers={"WWW-Authenticate":"Bearer"})
    try:        
        user = await verify_jwt_token(token=user_token_data.access_token, credentials_exception=credentials_exception)
        await get_user_by_email(user.email, session)                
    except HTTPException as e:
        raise e    
    token_blacklist.add(user_token_data.access_token)
    return {"Message":"Logged Out"}



        
        
    


    
    
    



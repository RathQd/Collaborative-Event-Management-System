from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.schema.token import TokenUserData, ReadToken
from app.config import settings
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/login')

token_blacklist = set()

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def create_jwt_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": int(expire.timestamp())})
    token =jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return token

async def create_refresh_jwt_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": int(expire.timestamp())})
    token =jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return token

async def verify_jwt_token(token: str, credentials_exception):    
    if token in token_blacklist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("email")
        id: int = payload.get("id")
        if email is None:
            raise credentials_exception
        if id is None:
            raise credentials_exception
        token_data = TokenUserData(email=email,id=id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Expired Token")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Invalid token")
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials", headers={"WWW-Authenticate":"Bearer"})
    token_data = await verify_jwt_token(token, credentials_exception)
    return token_data
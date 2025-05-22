from fastapi import HTTPException, status
from app.schema.User import RegisterUser, ReadUser
from app.utils.hash import hash, verify_hash
from sqlalchemy.exc import IntegrityError
from app.model.user import User

async def create_user(user: RegisterUser, session)->ReadUser:    
    try:        
        db_user = User(username=user.username, email=user.email, password_hashed=hash(user.password))
        session.add(db_user)
        session.commit()
    except IntegrityError:        
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered !")
    except Exception as e: 
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
    session.refresh(db_user)
    return db_user
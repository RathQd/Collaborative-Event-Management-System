from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class ReadUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attribute = True
    
    
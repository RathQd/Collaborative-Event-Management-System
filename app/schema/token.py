from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str

class TokenUserData(BaseModel):
    email: EmailStr = Field(...)
    id: int

class ReadToken(BaseModel):
    email: EmailStr = Field(...)
    token: Token
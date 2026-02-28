from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

class SignupCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr | None = None
    username: str
    password: str
    confirm_password: str
    
    @field_validator('username')
    @classmethod
    def vaildate_username(cls, value: str):
        print(value)
        return value.lower().strip()

class SignupResponse(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: EmailStr | None
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginCreate(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    access_type: str
    refresh_token: str

class UserCardResponse(BaseModel):
    id: int
    username: str


class TokenInput(BaseModel):
    refresh_token: str | None
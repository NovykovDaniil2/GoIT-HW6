from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str 
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional: Optional[str]

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }



class ContactResponse(ContactModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


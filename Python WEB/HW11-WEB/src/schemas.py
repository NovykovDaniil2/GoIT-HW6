from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


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



from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    email: str
    password: str
    first_name = str
    last_name = str


class UserUpdate(UserBase):
    password: Optional[str] = None

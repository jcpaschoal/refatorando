from typing import Optional
from unicodedata import name
from pydantic import BaseModel, EmailStr, Field, validator

class AddressBase(BaseModel):
    address_id: int | None
    user_id: int | None
    postal_code_id: int | None
    address: str | Field(None, min_length=4, max_length=200)
    details: str | Field(None, min_length=4, max_length=200)
    description: str | None = Field(None, min_length=4, max_length=45)

    
class AddressCreate(UserBase):
    address_id: int
    user_id: int
    postal_code_id: int
    address: str | Field(..., min_length=4, max_length=200)


class AddressUpdate(AddressBase):
    pass
  
class AddressResponse(AddressBase):
    address_id: Optional[int] = None

    class Config:
        orm_mode = True

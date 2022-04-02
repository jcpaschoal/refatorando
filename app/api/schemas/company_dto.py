from typing import Optional
from unicodedata import name
from pydantic import BaseModel, EmailStr, Field, validator

class CompanyBase(BaseModel):
    company_id: int | None
    owner_id: int | None
    description: str | None = Field(None, min_length=4, max_length=45)
    
class CompanyCreate(UserBase):
    company_id: int
    owner_id: int
    description: str = Field(..., min_length=4, max_length=45)


class CompanyUpdate(CompanyBase):
    pass
 
 
class CompanyResponse(CompanyBase):
    company_id: Optional[int] = None

    class Config:
        orm_mode = True

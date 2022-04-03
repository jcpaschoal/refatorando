from tabnanny import check
from typing import Any, Optional, Dict
from unicodedata import category
from sqlalchemy.orm import Session
from core.utils import get_session
from database.models.user import ManagerCategory
from pydantic import BaseModel, EmailStr, Field, validator

#TODO criar endpoit get para categorias
def load_manager_categories(db: Session) -> Dict:
    categories_dict = dict()
    categories = db.query(ManagerCategory).all()
    for category in categories:
        categories_dict[category.manager_category_id] = category.description
        categories_dict[category.description] = category.manager_category_id
    return categories_dict


CATEGORIES = load_manager_categories(get_session())

def check_category(category) -> int:
    if category_id := CATEGORIES.get(category, None) is not None and isinstance(
        category, str
    ):
        return category_id
    if description := CATEGORIES.get(category, None) is not None and isinstance(
        category, int
    ):
        return CATEGORIES[description]
    return None


def nif_must_be_valid(nif: str) -> bool:
    nif = str(nif) if isinstance(nif, int) else nif
    len_nif = len(nif)

    if (
        nif[0:1] not in ["1", "2", "3", "5", "6", "8"]
        and nif[0:2] not in ["45", "70", "71", "72", "77", "79", "90", "91", "98", "99"]
        and len_nif != 9
    ):
        return False
    sumAux = 0
    for i in range(9, 1, -1):
        sumAux += i * (int(nif[len_nif - i]))

    module = sumAux % 11

    nif_without_last_digit = nif[0:8]
    if module == 0 or module == 1:
        return f"{nif_without_last_digit}0" == nif
    else:
        return f"{nif_without_last_digit}{11-module}" == nif


class UserBase(BaseModel):
    email: EmailStr | None
    first_name: str | None = Field(None, min_length=4, max_length=45)
    last_name: str | None = Field(None, min_length=4, max_length=45)
    is_owner: bool | None
    category: int | str | None
    nif: int | str = None

    @validator("nif")
    def check_nif(cls, v):
        if v is None:
            return v
        if nif_must_be_valid(v) is False:
            raise ValueError("invalid nif")
        return v

    @validator("category")
    def check_category(cls, v):
        if v is None:
            return v
        if check_category(v) is None:
            raise ValueError("invalid category")
        return v


class UserCreate(UserBase):
    email: EmailStr
    # Minimum eight characters, at least one letter, one number and one special character:
    password: str = Field(
        ...,
        min_length=4,
        max_length=45,
        regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
        description="The price must be greater than zero",
    )
    first_name: str = Field(..., min_length=4, max_length=45)
    last_name: str = Field(..., min_length=4, max_length=45)


class UserUpdate(UserBase):
    # Minimum eight characters, at least one letter, one number and one special character:
    password: str | None = Field(
        None,
        min_length=4,
        max_length=45,
        regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
    )


class UserResponse(UserBase):
    class Config:
        orm_mode = True

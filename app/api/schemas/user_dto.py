from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


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
    nif: int | None
    is_owner: bool | None
    is_manager: bool | None

    @validator("nif")
    def check_nif(cls, v):
        if nif_must_be_valid(v) is False:
            raise ValueError("invalid nif")
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
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

from fastapi import APIRouter, Depends, HTTPException, Path
from core.utils import get_db_session
import api.service as service
from sqlalchemy.orm import Session
import api.schemas as schemas
from typing import Any


router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user_in: schemas.UserCreate, db: Session = Depends(get_db_session)
) -> Any:

    user = service.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists in the sytem,",
        )

    user = service.user.create(db, obj_in=user_in)

    return user_in


# TODO retirar parametro do id e pegar do token
@router.delete("/{user_id}", status_code=200)
def deactivate_user(
    user_id: int = Path(..., title="The id of the user to delete"),
    db: Session = Depends(get_db_session),
) -> Any:

    user = service.user.get_by_id(db, 1)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User does not exists",
        )

    user = service.user.deactivate_user(db, user)
    return {"user_id": user.user_id}


# user/address
@router.get("/address", response_model=schemas.AddressResponse)
def add_address(
    address_in: schemas.AddressCreate, db: Session = Depends(get_db_session)
):
    return address_in


@router.post("/company", response_model=schemas.CompanyResponse)
def add_contact(
    company_in: schemas.CompanyCreate, db: Session = Depends(get_db_session)
):
    return company_in

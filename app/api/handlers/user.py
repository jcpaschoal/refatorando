from tabnanny import check
from fastapi import APIRouter, Depends, HTTPException, Path, Security
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
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


@router.delete("/", status_code=200)
def deactivate_user(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> Any:

    service.user.deactivate_user(db, current_user)


@router.put(
    "/",
    status_code=200,
    response_model=schemas.UserResponse,
    response_model_exclude_none=True,
)
def update_user(
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> Any:

    if user_in.email is not None:
        if service.user.check_if_email_already_exists(
            db, user_in.email, current_user.email
        ):
            raise HTTPException(
                status_code=400,
                detail="Email already exists in the sytem,",
            )

    user = service.user.update_user(db, user_in, current_user)
    return user


@router.get("/address", response_model=schemas.AddressResponse)
def get_address(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
    page_num: int = 1, page_size: int = 10
):
    pass


@router.post("/address", response_model=schemas.AddressResponse)
def add_address(
    obj_in: schemas.AddressCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    address = service.user.add_address(db, obj_in, current_user)
    return address


@router.put("/address", response_model=schemas.AddressResponse)
def update_address(
    obj_in: schemas.AddressUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    address = service.user.update_address(db, obj_in, current_user)

    if not address:
        raise HTTPException(status_code=400, detail="Address does not exists")

    return address


@router.delete("/address/{id}")
def delete_address(
    address_id: int = Path(..., title="The id of the address"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    address = service.user.delete_address(db, address_id, current_user)

    if not address:
        raise HTTPException(status_code=400, detail="Address does not exists")

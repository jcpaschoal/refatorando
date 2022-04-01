from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.utils import get_db_session
import api.schemas as schemas
import api.service_layer as service

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db_session)) -> Any:
    
    print(user_in)
    user = service.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists in the sytem,",
        )
    
    user = service.user.create(db, obj_in=user_in)
    
    return user

# TODO pegar id do token
@router.delete("/", response_model=schemas.UserResponse, status_code=200)
def deactivate_user(db: Session = Depends(get_db_session)) -> Any:

    user = service.user.get_by_id(db, 1)
    
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User does not exists",
        )
        
    user = service.user.deactivate_user(db, user)
    return user


@router.post("/address", response_model=schemas.UserResponse)
def add_address(user_in: schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_obj = service.user.create(db, user_in)
    return schemas.UserResponse(**db_obj)


@router.post("/company", response_model=schemas.UserResponse)
def add_contact(user_in: schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_obj = service.user.create(db, user_in)
    return schemas.UserResponse(**db_obj)


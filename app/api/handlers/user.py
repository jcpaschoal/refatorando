from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from core.utils import get_db_session
import api.schemas as schemas
import api.service_layer as service

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db_session)):
    print(user_in)
    db_obj = service.user.create(db, user_in)
    return schemas.UserResponse(**db_obj)


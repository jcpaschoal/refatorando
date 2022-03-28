from re import U
from database.repository import SqlAlchemyRepository
from fastapi.encoders import jsonable_encoder
from core.auth import get_password_hash
from database.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
import api.schemas as schemas
from typing import Optional, Any


class UserService:

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.user_id == id).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        db_obj=User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )   
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_address(self, db: Session):
        pass

    def add_contact(self, db: Session):
        pass

    def update_user(self, db: Session, obj_in: schemas.UserUpdate) -> User:
        pass

    def deactivate_user(self, db: Session, db_obj: User) -> Any:
        db_obj.active = False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.user_id
        


user = UserService()

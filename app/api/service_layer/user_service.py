from database.repository import SqlAlchemyRepository
from fastapi.encoders import jsonable_encoder
from core.auth import get_password_hash
from database.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
import api.schemas as schemas
from typing import Optional


class UserService:
    def __init__(self):
        self.repository = SqlAlchemyRepository(User)

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: schemas.UserCreate) -> User:
        if self.get_by_email(db, obj_in.email):
            raise HTTPException(status_code=400, detail="Email already in use")
        obj_in = jsonable_encoder(obj_in)
        obj_in["password"] = get_password_hash(obj_in['password'])
        return self.create(db, obj_in)


user = UserService()

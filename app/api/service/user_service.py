from lib2to3.pgen2.token import OP
from database.repository import SqlAlchemyRepository
from fastapi.encoders import jsonable_encoder
from core.auth import get_password_hash, verify_password
from database.models.user import User, Owner, Manager, Role, UserRole
from database.models.address import Address
from database.models.contact import Contact

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
    
    @staticmethod
    def get_role(db: Session, role: str) -> Optional[Role]:
        role = db.query(Role).filter(Role.name == role).first()
        return role
    
    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        roles = []
        user_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        db.add(user_obj)
        db.flush()
        db.refresh(user_obj)
        roles.append(self.get_role(db, "user"))

        if obj_in.is_owner:
            owner_obj = Owner(user_id=user_obj.user_id)
            db.add(owner_obj)
            roles.append(self.get_role(db, "owner"))
        if obj_in.category:
            manager_obj = Manager(user_id=user_obj.user_id, manager_category_id=obj_in.category)
            db.add(manager_obj)
            roles.append(self.get_role(db, "manager"))
        
        if roles:
            user_obj.roles = [role for role in roles]
            db.add(user_obj)
        
        db.commit()
        return user_obj

    def add_address(self, db: Session, address: schemas.AddressCreate):
        pass

    def update_contact(self, db: Session):
        pass

    def delete_contact(self, db: Session):
        pass

    def add_contact(self, db: Session, contact: str) -> Contact:

        pass

    def update_contact(self, db: Session):
        pass

    def delete_contact(self, db: Session):
        pass

    def update_user(self, db: Session, obj_in: schemas.UserUpdate) -> User:
        pass

    def deactivate_user(self, db: Session, db_obj: User) -> Any:
        db_obj.active = False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.user_id

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = UserService()

from hashlib import new
from lib2to3.pgen2.token import OP
from database.repository import SqlAlchemyRepository
from fastapi.encoders import jsonable_encoder
from core.auth import get_password_hash, verify_password
from database.models.user import User, Owner, Manager, Role, ManagerCategory
from database.models.address import Address
from database.models.contact import Contact

from sqlalchemy.orm import Session
from fastapi import HTTPException
import api.schemas as schemas
from typing import Optional, Any


class UserService(SqlAlchemyRepository):
    def __init__(self):
        self.roles = None

    @staticmethod
    def get_manager_category(db: Session, category: str) -> Optional[ManagerCategory]:
        return db.query(ManagerCategory).filter(ManagerCategory.description == category)

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.user_id == id).first()

    @staticmethod
    def get_owner_by_user_id(db: Session, id: Any) -> Optional[Owner]:
        return db.query(Owner).filter(Owner.user_id == id).first()

    @staticmethod
    def get_manager_by_user_id(db: Session, id: Any) -> Optional[Manager]:
        return db.query(Manager).filter(Manager.user_id == id).first()

    def load_role(self, db: Session, role: str) -> Optional[Role]:
        if not self.roles:
            self.roles = dict()
            self.roles["owner"] = db.query(Role).filter(Role.name == "owner").first()
            self.roles["manager"] = db.query(Role).filter(Role.name == "manager").first()
            self.roles["user"] = db.query(Role).filter(Role.name == "user").first()

        return self.roles[role]

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
        roles.append(self.load_role(db, "user"))

        if obj_in.is_owner:
            owner_obj = Owner(user_id=user_obj.user_id)
            db.add(owner_obj)
            roles.append(self.load_role(db, "owner"))
        if obj_in.category:
            manager_obj = Manager(
                user_id=user_obj.user_id, manager_category_id=obj_in.category
            )
            db.add(manager_obj)
            roles.append(self.load_role(db, "manager"))

        user_obj.roles = [role for role in roles]
        db.add(user_obj)
        db.commit()
        return user_obj

    def add_address(
        self, db: Session, address: schemas.AddressCreate, db_obj: User
    ) -> Address:
        obj_in_data = address.dict()
        obj_in_data["user_id"] = db_obj.user_id
        return super().create(db=db, db_obj=Address, obj_in=obj_in_data)

    def get_address(
        self, db: Session, address: schemas.AddressCreate, db_obj: User
    ) -> Address:
        pass

    def delete_address(
        self, db: Session, address: schemas.AddressUpdate, db_obj: User
    ) -> Address:
        pass

    def update_address(self, db: Session):
        pass

    def delete_contact(self, db: Session):
        pass

    def add_contact(self, db: Session, contact: str) -> Contact:

        pass

    def update_contact(self, db: Session):
        pass

    def delete_contact(self, db: Session):
        pass

    def update_user(self, db: Session, obj_in: schemas.UserUpdate, user_obj: User) -> User:
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if (password := update_data.get("password", None)) is not None:
            update_data["password"] = get_password_hash(password)

        
        if obj_in.category is not None:
            manager = self.get_manager_by_user_id(db, user_obj.user_id)
            if manager is None:
                manager_obj = Manager(user_id=user_obj.user_id, manager_category_id=obj_in.category)
                db.add(manager_obj)
            elif manager.manager_category_id != obj_in.category:
                manager.manager_category_id = obj_in.category
                db.add(manager)
                 
                    
        return super().update(db=db, db_obj=user_obj, obj_in=update_data)

    def deactivate_user(self, db: Session, user_obj: User) -> Any:
        user_obj.active = False
        db.add(user_obj)
        db.commit()
        return user_obj.user_id

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


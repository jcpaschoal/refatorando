from sqlite3 import adapt
from tkinter.messagebox import NO
from database.repository import SqlAlchemyRepository
from fastapi.encoders import jsonable_encoder
from core.auth import get_password_hash, verify_password
from database.models.user import User, Owner, Manager, Role, ManagerCategory
from database.models.address import Address
from database.models.contact import Contact

from sqlalchemy.orm import Session
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

    @staticmethod
    def get_role(db: Session, role: Any) -> Optional[Role]:
        return db.query(Role).filter(Role.name == role).first()

    def check_if_email_already_exists(
        self, db: Session, email: str, user_obj: User
    ) -> bool:
        user = self.get_by_email(db, email)
        if user is None:
            return False
        if user_obj.user_id != user.user_id:
            return True
        return False

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
            manager_obj = Manager(
                user_id=user_obj.user_id, manager_category_id=obj_in.category
            )
            db.add(manager_obj)
            roles.append(self.get_role(db, "manager"))

        user_obj.roles = roles
        db.add(user_obj)
        db.commit()
        return user_obj

    def add_address(
        self, db: Session, address: schemas.AddressCreate, db_obj: User
    ) -> Address:
        obj_in_data = address.dict(exclude_unset=True)
        obj_in_data["user_id"] = db_obj.user_id
        return super().create(db=db, db_obj=Address, obj_in=obj_in_data)

    def get_address(
        self, db: Session, user_obj: User
    ) -> Address:
        pass    

    def delete_address(self, db: Session, address_id: int, user_obj: User) -> Address:
        if (
            address := db.query(Address)
            .filter(Address.address_id == address_id)
            .first()
        ) is not None:
            for user_address in user_obj.address:
                if user_address.address_id == address.address_id:
                    db.delete(address)
                    db.commit()
                    return address_id
        return None

    def update_address(
        self, db: Session, address: schemas.AddressUpdate, user_obj: User
    ) -> Address:
        if (
            address := db.query(Address)
            .filter(Address.address_id == address.address_id)
            .first()
        ) is not None:
            for user_address in user_obj.address:
                if user_address.address_id == address.address_id:
                    obj_in_data = address.dict(exclude_unset=True)
                    obj_in_data = address["user_id"] = user_obj.user_id
                    return super().update(db, db_obj=address, obj_in=obj_in_data)
        return None


    def add_contact(self, db: Session, contact: str) -> Contact:

        pass

    def update_contact(self, db: Session):
        pass

    def delete_contact(self, db: Session):
        pass

    def activate_role(self, db: Session, role: str, user_obj: User) -> User:
        roles = [role for role in user_obj.roles]
        if (add_role := self.get_role(db, role)) is not None:
            roles.append(add_role)
        user_obj.roles = roles
        return user_obj

    def deactivate_role(self, db: Session, role: str, user_obj: User) -> User:
        if (deleted_role := self.get_role(db, role)) is not None:
            user_obj.roles = [
                user_role
                for user_role in user_obj.roles
                if user_role.name != deleted_role.name
            ]
        return user_obj

    # TODO expirar sessao depois de atualizar campos de alteracao de tipo de usuario / refatorar if em metodos
    def update_user(
        self, db: Session, obj_in: schemas.UserUpdate, user_obj: User
    ) -> User:
        update_data = obj_in.dict(exclude_unset=True)

        if (password := update_data.get("password", None)) is not None:
            update_data["password"] = get_password_hash(password)

        if obj_in.category or obj_in.is_manager:
            manager = self.get_manager_by_user_id(db, user_obj.user_id)

            if manager is not None:
                if obj_in.is_manager is False and manager.active is True:
                    user_obj = self.deactivate_role(db, "manager", user_obj)
                    manager.active = False
                    db.add(manager)

                if obj_in.category:
                    if (
                        manager.active is True
                        and manager.manager_category_id != obj_in.category
                    ):
                        manager.manager_category_id = obj_in.category
                        db.add(manager)

                if (
                    obj_in.is_manager is True
                    and obj_in.category is None
                    and manager.active is False
                ):
                    manager.active = True
                    db.add(manager)
                    user_obj = self.activate_role(db, "manager", user_obj)

            if manager is None and obj_in.is_manager is not False and obj_in.category:
                user_obj = self.activate_role(db, "manager", user_obj)
                manager = Manager(
                    user_id=user_obj.user_id, manager_category_id=obj_in.category
                )
                db.add(manager)

        if obj_in.is_owner is not None:
            owner = self.get_owner_by_user_id(db, user_obj.user_id)

            if owner is not None:
                if owner.active is True and obj_in.is_owner is False:
                    user_obj = self.deactivate_role(db, "owner", user_obj)
                    owner.active = False
                    db.add(owner)

                if owner.active is False and obj_in.is_owner is True:
                    user_obj = self.activate_role(db, "owner", user_obj)
                    owner.active = True
                    db.add(owner)

            if owner is None and obj_in.is_owner is not False:
                user_obj = self.activate_role(db, "owner", user_obj)
                owner = Owner(user_id=user_obj.user_id)
                db.add(owner)

        update_data["roles"] = user_obj.roles
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

from msilib import Table
from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    BOOLEAN,
    VARCHAR,
    Enum as ENUM,
    DECIMAL,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from .company import CompanyManager
from .base_model import Base
from enum import Enum


class Encoder(str, Enum):
    bcrypt = "bcrypt"
    scrypt = "scrypt"


UserRole = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("role_id", Integer, ForeignKey("role.role_id"), nullable=False),
)

RolePermission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("role.role_id"), nullable=False),
    Column(
        "permission_id", Integer, ForeignKey("permission.permission_id"), nullable=False
    ),
)


class Permission(Base):
    permission_id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(45), nullable=False, index=True, unique=True)
    description = Column(VARCHAR(45), nullable=False, index=False, unique=True)


class Role(Base):
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(45), nullable=False, index=True, unique=True)
    description = Column(VARCHAR(45), nullable=False, index=False, unique=True)
    permissions = relationship("Permission", secondary=RolePermission)


class User(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR(45), nullable=False, index=True, unique=True)
    first_name = Column(VARCHAR(45), nullable=False, index=True)
    last_name = Column(VARCHAR(45), nullable=False, index=True)
    password_encoder = Column(ENUM(Encoder), nullable=False, default=Encoder.bcrypt)
    password = Column(CHAR(60), nullable=False)
    active = Column(BOOLEAN, nullable=False, default=True)
    nif = Column(Integer, nullable=True)
    roles = relationship("Role", secondary=UserRole)


class ManagerCategory(Base):
    __tablename__ = "manager_category"
    manager_category_id = Column(Integer, primary_key=True, index=True)
    description = Column(VARCHAR(45), nullable=False, unique=True)


class Manager(Base):
    manager_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    manager_category_id = Column(
        Integer, ForeignKey("manager_category.manager_category_id"), nullable=False
    )
    rating = Column(DECIMAL(3, 2), nullable=True, default=0)
    company = relationship(
        "Company", secondary=CompanyManager, back_populates="managers"
    )


class Owner(Base):
    owner_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

from sqlalchemy import Column, Integer, CHAR, BOOLEAN, VARCHAR, Enum as ENUM
from .base_model import Base
from sqlalchemy.orm import relationship
from enum import Enum


class Encoder(str, Enum):
    bcrypt = "bcrypt"
    scrypt = "scrypt"


class User(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR(45), nullable=False, index=True, unique=True)
    first_name = Column(VARCHAR(45), nullable=False, index=True)
    last_name = Column(VARCHAR(45), nullable=False, index=True)
    password_encoder = Column(ENUM(Encoder), nullable=False, default=Encoder.bcrypt)
    password = Column(CHAR(60), nullable=False)
    active = Column(BOOLEAN, nullable=False, default=True)
    nif = Column(Integer, nullable=True)
    


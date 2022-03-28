from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, Enum as ENUM
from .base_model import Base
from enum import Enum


class ContactType(str, Enum):
    fax = "fax"
    movel = "movel"
    fixo = "fixo"


class Contact(Base):
    contact_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    contact_type = Column(ENUM(ContactType), nullable=False)
    number = Column(VARCHAR(15), nullable=False, index=True)
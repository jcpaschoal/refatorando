from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    BOOLEAN,
    VARCHAR,
    Enum as ENUM,
    DECIMAL,
    ForeignKey,
)
from .base_model import Base
from sqlalchemy.orm import relationship
from enum import Enum


class Company(Base):
    company_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owner.owner_id"), nullable=False)
    name = Column(VARCHAR(45), nullable=False, index=True)

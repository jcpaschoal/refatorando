from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from database.models.base_model import Base
from sqlalchemy.orm import relationship


class PostalCode(Base):
    __tablename__ = "postal_code"
    postal_code_id = Column(Integer, primary_key=True, index=True)
    city = Column(VARCHAR(50), nullable=False, unique=True)
    address = relationship("address")


class Address(Base):
    address_id = Column(Integer, primary_key=True)
    postal_code_id = Column(Integer, ForeignKey("postal_code.postal_code_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False, index=True)
    address = Column(VARCHAR(100), nullable=False, index=True)
    details = Column(VARCHAR(200),  nullable=True)


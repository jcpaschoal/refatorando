from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base_model import Base


CompanyManager = Table(
    "company_manager",
    Base.metadata,
    Column("manager_id", Integer, ForeignKey("manager.manager_id"), nullable=False),
    Column("company_id", Integer, ForeignKey("company.company_id"), nullable=False),
)


class Company(Base):
    company_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owner.owner_id"), nullable=False)
    name = Column(VARCHAR(45), nullable=False, index=True)
    managers = relationship(
        "Manager", secondary=CompanyManager, back_populates="company"
    )

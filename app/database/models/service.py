from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, BOOLEAN, DECIMAL
from .base_model import Base


class ServiceCategory(Base):
    __tablename__ = "service_category"
    service_category_id = Column(Integer, primary_key=True)
    description = Column(VARCHAR(45), nullable=False, unique=True)


class Service(Base):
    service_id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("manager.manager_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    training_plan_id = Column(
        Integer, ForeignKey("training_plan.training_plan_id"), nullable=False
    )
    service_category_id = Column(
        Integer, ForeignKey("service_category.service_category_id"), nullable=False
    )
    rating = Column(DECIMAL(3, 2), nullable=True, default=0)
    status = Column(BOOLEAN, nullable=False, default=False)

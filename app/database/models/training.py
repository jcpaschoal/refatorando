from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    VARCHAR,
    BOOLEAN,
    DECIMAL,
    DATETIME,
    TIME,
    DATE,
    JSON,
)
from .base_model import Base


class TrainingCategory(Base):
    __tablename__ = "training_category"
    training_category_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(45), unique=True, nullable=False)


class TrainingPlan(Base):
    __tablename__ = "training_plan"
    training_plan_id = Column(Integer, primary_key=True)
    training_plan_category = Column(
        Integer, ForeignKey("training_category.training_category_id"), nullable=False
    )
    expiration_date = Column(DATE, nullable=False)
    price = Column(DECIMAL(4, 2), nullable=False)
    description = Column(VARCHAR(200), nullable=False)
    details = Column(JSON, nullable=True)
    status = Column(BOOLEAN, nullable=False, default=True)
    number_of_sessions = Column(Integer, nullable=True)
    description = Column(VARCHAR(200), nullable=True)


class Session(Base):
    session_id = Column(Integer, primary_key=True)
    training_plan_id = Column(
        Integer, ForeignKey("training_plan.training_plan_id"), nullable=False
    )
    date = Column(DATETIME, nullable=False)
    duration = Column(TIME, nullable=False)

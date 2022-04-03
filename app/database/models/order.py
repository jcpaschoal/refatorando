from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    VARCHAR,
    Enum as ENUM,
    DECIMAL,
    BOOLEAN,
    DATETIME,
    Table,
)
from sqlalchemy.orm import relationship
from .base_model import Base
from enum import Enum


InvoiceOrder = Table(
    "invoice_order",
    Base.metadata,
    Column("invoice_id", Integer, ForeignKey("invoice.invoice_id"), nullable=False),
    Column("order_id", Integer, ForeignKey("order.order_id"), nullable=False),
)


class PaymentCategory(str, Enum):
    mbway = "mbway"
    paypal = "paypal"
    credit_card = "credit_card"


class Invoice(Base):
    invoice_id = Column(Integer, primary_key=True)
    payment_category = Column(ENUM(PaymentCategory), nullable=False)
    total = Column(DECIMAL(4, 2), nullable=False, index=True)
    managers = relationship("Order", secondary=InvoiceOrder, back_populates="invoice")


class Order(Base):
    order_id = Column(Integer, primary_key=True)
    pricing_policy_id = Column(
        Integer, ForeignKey("pricing_policy.pricing_policy_id"), nullable=False
    )
    service_id = Column(Integer, ForeignKey("service.service_id"), nullable=False)
    amount = Column(DECIMAL(4, 2), nullable=False)
    amount_discounted = Column(DECIMAL(4, 2), nullable=False)
    payment_date = Column(DATETIME, nullable=True)
    status = Column(BOOLEAN, nullable=False, default=False)
    invoices = relationship("Invoice", secondary=InvoiceOrder, back_populates="order")


class PricingPolicy(Base):
    __tablename__ = "pricing_policy"
    pricing_policy_id = Column(Integer, primary_key=True)
    discount = Column(DECIMAL(3, 2), nullable=False)
    name = Column(VARCHAR(40), nullable=False)

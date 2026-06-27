from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from database import Base


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PACKED = "Packed"
    SHIPPED = "Shipped"
    OUT_FOR_DELIVERY = "Out For Delivery"
    DELIVERED = "Delivered"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    status = Column(SQLEnum(OrderStatus),default=OrderStatus.PENDING)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
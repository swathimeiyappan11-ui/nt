from pydantic import BaseModel
from models import OrderStatus


class OrderCreate(BaseModel):
    customer_name: str


class OrderUpdate(BaseModel):
    status: OrderStatus
    latitude: float
    longitude: float

class OrderResponse(BaseModel):
    id:int
    customer_name: str
    status: OrderStatus
    latitude: float
    longitude: float

    class Config:
        from_attributes = True 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import *
from schemas import *


async def create_order(db,customer_name):
    order = Order(customer_name=customer_name)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def get_order(db,order_id):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    return order


async def update_order(db: AsyncSession,order_id: int,data: OrderUpdate):
    order = await get_order(db, order_id)
    if not order:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    await db.commit()
    await db.refresh(order)
    return order
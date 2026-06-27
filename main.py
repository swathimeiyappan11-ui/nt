from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas
import crud
from contextlib import asynccontextmanager
from database import Base, engine
from fastapi import Request
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
connections = {} #----store active web socket user

@app.post("/orders")
async def create_order(
    order: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db,order.customer_name)

templates = Jinja2Templates(directory="templates")

@app.get("/track/{order_id}")
async def track_order(request: Request,order_id: int):
    return templates.TemplateResponse(
        request=request,
        name="tracking.html",
        context={
            "order_id": order_id
        }
    )


@app.websocket("/ws/{order_id}")
async def websocket_endpoint(websocket: WebSocket,order_id: int):
    await websocket.accept()
    connections[order_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except:
        connections.pop(order_id, None)


@app.put("/orders/{order_id}")
async def update_order(order_id: int,data: schemas.OrderUpdate,db: AsyncSession = Depends(get_db)):
    order = await crud.update_order(db,order_id,data)
    if not order:
        return {"message": "Order not found"}
    if order_id in connections:
        await connections[order_id].send_json( data.model_dump())
    return order
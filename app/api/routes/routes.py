from fastapi import APIRouter
from app.schemas.schemas import ItemCreate

routes = APIRouter(prefix="/api/v1")


@routes.get("/health")
def health_check():
    return {"status": "ok"}


@routes.post("/items")
def create_item(item:ItemCreate):
    
    return "item created"

@routes.get("/items/{id}")
def get_item(id: int):
    return f"item id {id}"


@routes.post("/items/{id}/sell")
def sell_item(id: int):
    return f"item {id} sold"


@routes.post("/items/{id}/restock")
def restock_item(id: int):
    return f"item {id} restocked"


@routes.get("/items/low-stock")
def get_low_stock_items():
    return {"items": []}
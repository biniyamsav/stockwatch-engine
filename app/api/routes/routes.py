from fastapi import APIRouter
from app.schemas.schemas import ItemCreate,StockOperation,ItemResponse
from app.db.database import SessionLocal
from app.db.models import Item
from sqlalchemy import select
from fastapi import HTTPException

routes = APIRouter(prefix="/api/v1")


@routes.get("/health")
def health_check():
    return {"status": "ok"}


@routes.post("/items")
def create_item(item:ItemCreate):
    db = SessionLocal()

    new_item = Item(
        name=item.name,
        sku=item.sku,
        quantity=item.quantity,
        low_stock_threshold=item.low_stock_threshold
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@routes.get("/items/{id}")
def get_item(id: int):
    db = SessionLocal()

    item = db.execute(
        select(Item).where(Item.id == id)
    ).scalar_one_or_none()

    db.close()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
@routes.post("/items/{id}/sell", response_model=ItemResponse)
def sell_item(id: int, operation: StockOperation):
    db = SessionLocal()

    item = db.execute(
        select(Item).where(Item.id == id)
    ).scalar_one_or_none()

    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    if operation.quantity > item.quantity:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    item.quantity -= operation.quantity

    db.commit()
    db.refresh(item)
    db.close()

    return item


@routes.post("/items/{id}/restock", response_model=ItemResponse)
def restock_item(id: int, operation: StockOperation):
    db = SessionLocal()

    item = db.execute(
        select(Item).where(Item.id == id)
    ).scalar_one_or_none()

    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    item.quantity += operation.quantity

    db.commit()
    db.refresh(item)
    db.close()

    return item


@routes.get("/items/low-stock", response_model=list[ItemResponse])
def get_low_stock_items():
    db = SessionLocal()

    items = db.execute(
        select(Item).where(Item.quantity <= Item.low_stock_threshold)
    ).scalars().all()

    db.close()

    return items
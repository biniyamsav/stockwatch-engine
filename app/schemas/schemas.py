from pydantic import BaseModel,Field

class ItemCreate(BaseModel):
    name:str
    sku:str
    quantity: int = Field(ge=0)
    low_stock_threshold: int = Field(ge=0)
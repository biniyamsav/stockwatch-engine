from pydantic import BaseModel, Field, ConfigDict
class ItemCreate(BaseModel):
    name:str
    sku:str
    quantity: int = Field(ge=0)
    low_stock_threshold: int = Field(ge=0)
    
class ItemResponse(BaseModel):
    id: int
    name: str
    sku: str
    quantity: int
    low_stock_threshold: int

    model_config = ConfigDict(from_attributes=True)
    
class StockOperation(BaseModel):
    quantity: int = Field(gt=0)
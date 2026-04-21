from pydantic import BaseModel

class InventoryCreate(BaseModel):
    medicine_id: int
    stock: int
    price: int
from pydantic import BaseModel

class MedicineCreate(BaseModel):
    name: str
    description: str
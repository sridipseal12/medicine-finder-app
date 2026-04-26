from pydantic import BaseModel

class PharmacyCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float

class PharmacyResponse(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True
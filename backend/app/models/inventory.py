from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    stock = Column(Integer)
    price = Column(Integer)
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.medicine import Medicine
from app.schemas.medicine_schema import MedicineCreate

router = APIRouter(prefix="/medicine", tags=["Medicine"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    new_medicine = Medicine(
        name=medicine.name,
        description=medicine.description
    )
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine
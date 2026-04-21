from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pharmacy import Pharmacy
from app.schemas.pharmacy_schema import PharmacyCreate
from app.services.dependency import get_current_user

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_pharmacy(
    pharmacy: PharmacyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_pharmacy = Pharmacy(
        name=pharmacy.name,
        address=pharmacy.address,
        owner_id=current_user.id  # 🔥 important
    )

    db.add(new_pharmacy)
    db.commit()
    db.refresh(new_pharmacy)

    return new_pharmacy
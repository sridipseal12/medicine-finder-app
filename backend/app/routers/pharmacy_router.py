from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pharmacy import Pharmacy
from app.schemas.pharmacy_schema import PharmacyCreate
from app.services.dependency import get_current_user, require_role

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
    existing = db.query(Pharmacy).filter(
        Pharmacy.name == pharmacy.name,
        Pharmacy.address == pharmacy.address
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Pharmacy with same name already exists in this address"
        )
    new_pharmacy = Pharmacy(
        name=pharmacy.name,
        address=pharmacy.address,
        latitude=pharmacy.latitude,
        longitude=pharmacy.longitude,
        owner_id=current_user.id  # 🔥 important
    )

    db.add(new_pharmacy)
    # 🔥 ADD ROLE UPDATE HERE
    if current_user.role == "patient":
        current_user.role = "pharmacy_owner"
    db.commit()
    db.refresh(new_pharmacy)

    return new_pharmacy

@router.get("/all-pharmacies")
def get_all_pharmacies(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    return db.query(Pharmacy).all()


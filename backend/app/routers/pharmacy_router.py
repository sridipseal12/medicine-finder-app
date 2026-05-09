from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.pharmacy import Pharmacy
from app.schemas.pharmacy_schema import PharmacyCreate
from app.services.dependency import get_current_user, require_role, get_db

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])

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
        # `current_user` may be attached to a different SQLAlchemy Session
        # (created inside the auth dependency). Merge it into this request's
        # Session so `db.commit()` persists the role update.
        current_user = db.merge(current_user)
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


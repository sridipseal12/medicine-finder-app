from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.inventory import Inventory
from app.schemas.inventory_schema import InventoryCreate
from app.services.dependency import get_current_user
from app.models.pharmacy import Pharmacy

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_inventory(
    item: InventoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get user's pharmacy
    pharmacy = db.query(Pharmacy).filter(
        Pharmacy.owner_id == current_user.id
    ).first()

    new_item = Inventory(
        pharmacy_id=pharmacy.id,
        medicine_id=item.medicine_id,
        stock=item.stock,
        price=item.price
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
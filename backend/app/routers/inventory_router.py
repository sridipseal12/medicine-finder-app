from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.inventory import Inventory
from app.schemas.inventory_schema import InventoryCreate
from app.services.dependency import get_current_user
from app.models.pharmacy import Pharmacy
from app.models.inventory import Inventory
from app.models.medicine import Medicine

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

@router.get("/search")
def search_medicine(name: str, db: Session = Depends(get_db)):
    results = db.query(
        Medicine.name,
        Pharmacy.name,
        Pharmacy.address.label("address"), 
        Inventory.stock,
        Inventory.price
    ).join(
        Inventory, Medicine.id == Inventory.medicine_id
    ).join(
        Pharmacy, Pharmacy.id == Inventory.pharmacy_id
    ).filter(
        Medicine.name.ilike(f"%{name}%"),
        Inventory.stock > 0
    ).order_by(
        Inventory.price.asc()
    ).all()

    return [
        {
            "medicine": r[0],
            "pharmacy": r[1],
            "address": r[2],
            "stock": r[3],
            "price": r[4]
        }
        for r in results
    ]

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.inventory import Inventory
from app.schemas.inventory_schema import InventoryCreate
from app.services.dependency import get_current_user
from app.models.pharmacy import Pharmacy
from app.models.inventory import Inventory
from app.models.medicine import Medicine
import math

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

    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

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

@router.get("/search")
def search_medicine(
    name: str,
    user_lat: float,
    user_lon: float,
    max_price: int = None,
    min_stock: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(
        Medicine.name.label("medicine"),
        Pharmacy.name.label("pharmacy"),
        Pharmacy.address,
        Pharmacy.latitude,
        Pharmacy.longitude,
        Inventory.stock,
        Inventory.price
    ).join(
        Inventory, Inventory.medicine_id == Medicine.id
    ).join(
        Pharmacy, Pharmacy.id == Inventory.pharmacy_id
    ).filter(
        Medicine.name.ilike(f"%{name}%"),
        Inventory.stock > min_stock
    )

    if max_price is not None:
        query = query.filter(Inventory.price <= max_price)

    results = query.all()

    response = []

    for r in results:
        distance = math.sqrt(
            (r.latitude - user_lat)**2 +
            (r.longitude - user_lon)**2
        )

        response.append({
            "medicine": r.medicine,
            "pharmacy": r.pharmacy,
            "address": r.address,
            "stock": r.stock,
            "price": r.price,
            "distance": round(distance, 4)
        })

    response.sort(key=lambda x: (x["distance"], x["price"]))

    return response[:limit]
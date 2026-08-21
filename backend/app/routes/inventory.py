from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.services.audit_service import log_audit
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
async def list_inventory(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Inventory))
    return result.scalars().all()


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(payload: InventoryCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    inv = Inventory(**payload.dict())
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    await log_audit(db, "create", "inventory", inv.id, current_user.id)
    return inv


@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(inventory_id: int, payload: InventoryUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Inventory).where(Inventory.id == inventory_id))
    inv = result.scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(inv, key, value)
    await db.commit()
    await db.refresh(inv)
    await log_audit(db, "update", "inventory", inv.id, current_user.id)
    return inv

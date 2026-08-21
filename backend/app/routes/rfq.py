from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.rfq import RFQ
from app.schemas.rfq import RFQCreate, RFQUpdate, RFQResponse
from app.services.audit_service import log_audit
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[RFQResponse])
async def list_rfqs(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(RFQ))
    return result.scalars().all()


@router.post("/", response_model=RFQResponse, status_code=status.HTTP_201_CREATED)
async def create_rfq(payload: RFQCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    rfq = RFQ(**payload.dict())
    db.add(rfq)
    await db.commit()
    await db.refresh(rfq)
    await log_audit(db, "create", "rfq", rfq.id, current_user.id)
    return rfq


@router.get("/{rfq_id}", response_model=RFQResponse)
async def get_rfq(rfq_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(RFQ).where(RFQ.id == rfq_id))
    rfq = result.scalar_one_or_none()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
    return rfq


@router.put("/{rfq_id}", response_model=RFQResponse)
async def update_rfq(rfq_id: int, payload: RFQUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(RFQ).where(RFQ.id == rfq_id))
    rfq = result.scalar_one_or_none()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(rfq, key, value)
    await db.commit()
    await db.refresh(rfq)
    await log_audit(db, "update", "rfq", rfq.id, current_user.id)
    return rfq


@router.delete("/{rfq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rfq(rfq_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(RFQ).where(RFQ.id == rfq_id))
    rfq = result.scalar_one_or_none()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
    await db.delete(rfq)
    await db.commit()
    await log_audit(db, "delete", "rfq", rfq_id, current_user.id)

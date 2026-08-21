import json
import os
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.purchase_order import PurchaseOrder
from app.models.vendor import Vendor
from app.models.quotation import Quotation
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderApprove, PurchaseOrderResponse
from app.services.audit_service import log_audit
from app.services.po_generator import generate_po_pdf
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[PurchaseOrderResponse])
async def list_purchase_orders(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(PurchaseOrder))
    return result.scalars().all()


@router.post("/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_po(payload: PurchaseOrderCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    po = PurchaseOrder(**payload.dict())
    db.add(po)
    await db.commit()
    await db.refresh(po)
    await log_audit(db, "create", "purchase_order", po.id, current_user.id)
    return po


@router.post("/{po_id}/approve", response_model=PurchaseOrderResponse)
async def approve_po(po_id: int, payload: PurchaseOrderApprove, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == po_id))
    po = result.scalar_one_or_none()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    po.status = "approved"
    po.approved_by = payload.approved_by
    po.approved_at = datetime.utcnow()
    await db.commit()
    await db.refresh(po)

    ven_res = await db.execute(select(Vendor).where(Vendor.id == po.vendor_id))
    vendor = ven_res.scalar_one_or_none()
    rfq_res = await db.execute(select(Quotation).where(Quotation.id == po.quotation_id))
    quotation = rfq_res.scalar_one_or_none()
    items = json.loads(po.items or "[]")
    output_path = os.path.join("uploads", f"po_{po.po_number}.pdf")
    generate_po_pdf(
        {"po_number": po.po_number, "subtotal": float(po.subtotal or 0), "tax": float(po.tax or 0), "total_amount": float(po.total_amount or 0)},
        {"name": vendor.name if vendor else "", "email": vendor.email if vendor else ""},
        {"rfq_number": "", "title": ""},
        items,
        output_path,
    )
    await log_audit(db, "approve", "purchase_order", po.id, current_user.id)
    return po


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
async def get_po(po_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == po_id))
    po = result.scalar_one_or_none()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po

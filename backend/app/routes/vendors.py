from typing import List

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorEvaluateRequest, VendorEvaluateResponse, VendorUpdate, VendorResponse
from app.services.audit_service import log_audit
from app.services.starai import STARAI
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[VendorResponse])
async def list_vendors(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Vendor))
    return result.scalars().all()


@router.post("/ai/evaluate", response_model=VendorEvaluateResponse, name="evaluate_vendor")
async def evaluate_vendor(payload: VendorEvaluateRequest, current_user=Depends(get_current_active_user)):
    starai = STARAI()
    prompt = (
        "You are STAR AI, a procurement intelligence engine.\n"
        "Evaluate the following vendor and return ONLY valid JSON with this exact schema:\n"
        "{\n"
        '  "overall_score": 0,\n'
        '  "price_score": 0,\n'
        '  "delivery_score": 0,\n'
        '  "reliability_score": 0,\n'
        '  "terms_score": 0,\n'
        '  "risk": "Low",\n'
        '  "recommendation": "string"\n'
        "}\n\n"
        f"Vendor Data: {json.dumps(payload.dict())}\n"
        "Scoring rules:\n"
        "- overall_score: weighted 0-100 integer\n"
        "- price_score: 0-100 based on rating and market competitiveness\n"
        "- delivery_score: 0-100 based on avg_delivery_days (lower is better)\n"
        "- reliability_score: use reliability_score field directly scaled to 100\n"
        "- terms_score: 0-100 based on payment terms inferred from category\n"
        "- risk: Low, Medium, or High based on reliability and delivery\n"
        "- recommendation: 1-2 sentence concise recommendation\n"
    )

    try:
        completion = await starai.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="groq/compound",
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        content = completion.choices[0].message.content
        data = json.loads(content)
        return data
    except Exception as exc:
        raise HTTPException(status_code=500, detail="STAR AI evaluation failed") from exc


@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(payload: VendorCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    vendor = Vendor(**payload.dict())
    db.add(vendor)
    await db.commit()
    await db.refresh(vendor)
    await log_audit(db, "create", "vendor", vendor.id, current_user.id)
    return vendor


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    vendor = result.scalar_one_or_none()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(vendor_id: int, payload: VendorUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    vendor = result.scalar_one_or_none()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(vendor, key, value)
    await db.commit()
    await db.refresh(vendor)
    await log_audit(db, "update", "vendor", vendor.id, current_user.id)
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(vendor_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    vendor = result.scalar_one_or_none()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    await db.delete(vendor)
    await db.commit()
    await log_audit(db, "delete", "vendor", vendor_id, current_user.id)

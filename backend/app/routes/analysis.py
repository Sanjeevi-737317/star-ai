from typing import List

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.rfq import RFQ
from app.models.quotation import Quotation
from app.models.vendor_score import VendorScore
from app.models.vendor import Vendor
from app.schemas.analysis import AnalysisResponse, VendorScoreResponse
from app.services.audit_service import log_audit
from app.services.scoring import calculate_scores
from app.services.starai import STARAI
from app.services.risk_engine import analyze_risk
from app.services.tco_engine import calculate_tco
from app.utils import get_current_active_user

router = APIRouter()
starai = STARAI()


@router.post("/analyze/{rfq_id}", response_model=AnalysisResponse)
async def analyze_rfq(rfq_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(RFQ).where(RFQ.id == rfq_id))
    rfq = result.scalar_one_or_none()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    result = await db.execute(select(Quotation).where(Quotation.rfq_id == rfq_id, Quotation.status == "completed"))
    quotations = result.scalars().all()
    if not quotations:
        raise HTTPException(status_code=400, detail="No completed quotations found for this RFQ")

    rfq_data = {"id": rfq.id, "rfq_number": rfq.rfq_number, "title": rfq.title}
    quotation_dicts = []
    for q in quotations:
        extracted = json.loads(q.extracted_data or "{}")
        vendor_result = await db.execute(select(Vendor).where(Vendor.id == q.vendor_id))
        vendor = vendor_result.scalar_one_or_none()
        vendor_dict = {"id": vendor.id, "name": vendor.name} if vendor else {"id": q.vendor_id}
        quotation_dicts.append({
            "id": q.id,
            "vendor_id": q.vendor_id,
            "subtotal": q.subtotal,
            "total": q.total,
            "delivery_days": q.delivery_days,
            "payment_terms": q.payment_terms,
            "warranty": q.warranty,
            "shipping": q.shipping,
            "tax": q.tax,
            "items": extracted.get("items", []),
            "vendor": vendor_dict,
        })

    scores = calculate_scores(quotation_dicts, rfq_data)
    tco_results = []
    risk_results = []
    for score in scores:
        q = next(x for x in quotation_dicts if x["id"] == score["quotation_id"])
        v = q["vendor"]
        tco = calculate_tco(q, v)
        risk = analyze_risk(q, v, rfq_data)
        tco_results.append(tco)
        risk_results.append(risk)

    recommendation = await starai.get_recommendation(rfq_id, scores, tco_results, risk_results)

    old_scores = await db.execute(select(VendorScore).where(VendorScore.rfq_id == rfq_id))
    for old_score in old_scores.scalars().all():
        await db.delete(old_score)
    await db.commit()

    saved_scores = []
    for idx, score in enumerate(scores):
        q = next(x for x in quotation_dicts if x["id"] == score["quotation_id"])
        vs = VendorScore(
            quotation_id=score["quotation_id"],
            vendor_id=score["vendor_id"],
            rfq_id=rfq_id,
            price_score=score["price_score"],
            delivery_score=score["delivery_score"],
            quality_score=score.get("quality_score", 0.0),
            warranty_score=score.get("warranty_score", 0.0),
            payment_score=score["payment_score"],
            reliability_score=score["reliability_score"],
            final_score=score["final_score"],
            tco=tco_results[idx]["tco"],
            risk_score=risk_results[idx]["risk_score"],
            risk_level=risk_results[idx]["risk_level"],
            recommendation_rank=idx + 1,
            delivery_days=q.get("delivery_days"),
            payment_terms=q.get("payment_terms"),
        )
        db.add(vs)
        saved_scores.append(vs)
    await db.commit()
    for vs in saved_scores:
        await db.refresh(vs)

    vendor_map = {}
    for q in quotation_dicts:
        vendor_map[q["vendor_id"]] = q.get("vendor", {}).get("name")

    score_payload = []
    for vs in saved_scores:
        score_payload.append({
            "id": vs.id,
            "quotation_id": vs.quotation_id,
            "vendor_id": vs.vendor_id,
            "rfq_id": vs.rfq_id,
            "price_score": vs.price_score,
            "delivery_score": vs.delivery_score,
            "quality_score": vs.quality_score,
            "warranty_score": vs.warranty_score,
            "payment_score": vs.payment_score,
            "reliability_score": vs.reliability_score,
            "final_score": vs.final_score,
            "tco": vs.tco,
            "risk_score": vs.risk_score,
            "risk_level": vs.risk_level,
            "recommendation_rank": vs.recommendation_rank,
            "delivery_days": vs.delivery_days,
            "payment_terms": vs.payment_terms,
            "vendor_name": vendor_map.get(vs.vendor_id),
            "created_at": vs.created_at.isoformat() if vs.created_at else None,
        })

    await log_audit(db, "analyze", "rfq", rfq_id, current_user.id)
    return {"rfq_id": rfq_id, "scores": score_payload, "recommendation": recommendation}


@router.get("/results/{rfq_id}", response_model=AnalysisResponse)
async def get_analysis_results(rfq_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(VendorScore).where(VendorScore.rfq_id == rfq_id).order_by(VendorScore.recommendation_rank))
    scores = result.scalars().all()
    if not scores:
        raise HTTPException(status_code=404, detail="Analysis not found for this RFQ")
    recommendation = "Run analysis to generate a recommendation."
    vendor_map = {}
    for vs in scores:
        vendor_result = await db.execute(select(Vendor).where(Vendor.id == vs.vendor_id))
        vendor = vendor_result.scalar_one_or_none()
        if vendor:
            vendor_map[vs.vendor_id] = vendor.name
    score_payload = []
    for vs in scores:
        score_payload.append({
            "id": vs.id,
            "quotation_id": vs.quotation_id,
            "vendor_id": vs.vendor_id,
            "rfq_id": vs.rfq_id,
            "price_score": vs.price_score,
            "delivery_score": vs.delivery_score,
            "quality_score": vs.quality_score,
            "warranty_score": vs.warranty_score,
            "payment_score": vs.payment_score,
            "reliability_score": vs.reliability_score,
            "final_score": vs.final_score,
            "tco": vs.tco,
            "risk_score": vs.risk_score,
            "risk_level": vs.risk_level,
            "recommendation_rank": vs.recommendation_rank,
            "delivery_days": vs.delivery_days,
            "payment_terms": vs.payment_terms,
            "vendor_name": vendor_map.get(vs.vendor_id),
            "created_at": vs.created_at.isoformat() if vs.created_at else None,
        })
    return {"rfq_id": rfq_id, "scores": score_payload, "recommendation": recommendation}

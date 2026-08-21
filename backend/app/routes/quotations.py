import os
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.quotation import Quotation
from app.schemas.quotation import QuotationCreate, QuotationResponse
from app.services.quotation_parser import extract_text
from app.services.starai import STARAI

router = APIRouter()
starai = STARAI()


@router.get("/", response_model=List[QuotationResponse])
async def list_quotations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quotation))
    return result.scalars().all()


@router.post("/upload", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def upload_quotation(
    file: UploadFile = File(...),
    rfq_id: int = Form(...),
    vendor_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    quotation = Quotation(
        rfq_id=rfq_id,
        vendor_id=vendor_id,
        file_path=file_path,
        status="processing",
    )
    db.add(quotation)
    await db.commit()
    await db.refresh(quotation)

    try:
        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract text from file. For image files, ensure Tesseract OCR is installed. For PDFs, ensure the file contains selectable text.",
            )
        extracted = await starai.analyze_quotation(text)
        quotation.extracted_data = extracted.model_dump_json()
        quotation.subtotal = extracted.subtotal
        quotation.tax = extracted.tax
        quotation.shipping = extracted.shipping
        quotation.total = extracted.total
        quotation.delivery_days = extracted.delivery_days
        quotation.payment_terms = extracted.payment_terms
        quotation.warranty = extracted.warranty
        quotation.status = "completed"
        await db.commit()
        await db.refresh(quotation)

    except Exception:
        quotation.status = "failed"
        await db.commit()

    return quotation


@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(quotation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quotation).where(Quotation.id == quotation_id))
    quotation = result.scalar_one_or_none()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

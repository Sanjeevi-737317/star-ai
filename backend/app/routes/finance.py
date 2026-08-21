from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.finance import Finance
from app.schemas.finance import FinanceCreate, FinanceUpdate, FinanceResponse
from app.services.audit_service import log_audit
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[FinanceResponse])
async def list_finance(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Finance))
    return result.scalars().all()


@router.post("/", response_model=FinanceResponse, status_code=status.HTTP_201_CREATED)
async def create_finance(payload: FinanceCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    finance = Finance(**payload.dict())
    db.add(finance)
    await db.commit()
    await db.refresh(finance)
    await log_audit(db, "create", "finance", finance.id, current_user.id)
    return finance


@router.put("/{finance_id}", response_model=FinanceResponse)
async def update_finance(finance_id: int, payload: FinanceUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_active_user)):
    result = await db.execute(select(Finance).where(Finance.id == finance_id))
    finance = result.scalar_one_or_none()
    if not finance:
        raise HTTPException(status_code=404, detail="Finance record not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(finance, key, value)
    await db.commit()
    await db.refresh(finance)
    await log_audit(db, "update", "finance", finance.id, current_user.id)
    return finance

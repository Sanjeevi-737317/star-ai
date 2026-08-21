from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogResponse
from app.utils import get_current_active_user

router = APIRouter()


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    entity_type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    query = select(AuditLog)
    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)
    result = await db.execute(query.order_by(AuditLog.created_at.desc()))
    return result.scalars().all()

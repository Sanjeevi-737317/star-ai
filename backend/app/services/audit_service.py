import logging

logger = logging.getLogger(__name__)


async def log_audit(db, action: str, entity_type: str, entity_id: int | None, user_id: int | None, details: str | None = None):
    from app.models.audit_log import AuditLog
    from app.schemas.audit_log import AuditLogResponse

    entry = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        details=details,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

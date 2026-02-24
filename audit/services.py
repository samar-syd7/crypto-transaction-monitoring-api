from audit.models import AuditEvent


def log_audit_event(
    *,
    event_type: str,
    entity_type: str,
    entity_id,
    actor: str,
    metadata: dict,
):
    AuditEvent.objects.create(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        metadata=metadata,
    )
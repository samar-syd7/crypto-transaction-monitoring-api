from django.db import models

# Create your models here.
import uuid
from django.db import models


class AuditEvent(models.Model):
    """
    Append-only audit log.
    Never update. Never delete.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event_type = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField()

    actor = models.CharField(max_length=64)  # system / service / analyst

    metadata = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise RuntimeError("AuditEvent is append-only and cannot be updated")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise RuntimeError("AuditEvent cannot be deleted")
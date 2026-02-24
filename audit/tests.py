from django.test import TestCase
from audit.models import AuditEvent
import uuid


class AuditImmutabilityTest(TestCase):

    def test_audit_event_is_immutable(self):
        event = AuditEvent.objects.create(
            event_type="TEST_EVENT",
            entity_type="TestEntity",
            entity_id=uuid.uuid4(),
            actor="system",
            metadata={"key": "value"},
        )

        event.metadata = {}
        with self.assertRaises(RuntimeError):
            event.save()

        with self.assertRaises(RuntimeError):
            event.delete()
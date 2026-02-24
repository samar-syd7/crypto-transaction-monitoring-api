from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now

from .models import ComplianceCase
from .serializers import ComplianceCaseSerializer
from audit.services import log_audit_event
from config.permissions import IsComplianceAnalyst

class ComplianceCaseListAPIView(generics.ListAPIView):
    permission_classes = [IsComplianceAnalyst]
    queryset = ComplianceCase.objects.exclude(status="CLOSED")
    serializer_class = ComplianceCaseSerializer
    
class ComplianceCaseUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsComplianceAnalyst]
    queryset = ComplianceCase.objects.all()
    serializer_class = ComplianceCaseSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == "CLOSED" and instance.closed_at is None:
            instance.closed_at = now()
            instance.save(update_fields=["closed_at"])

        log_audit_event(
            event_type="COMPLIANCE_CASE_UPDATED",
            entity_type="ComplianceCase",
            entity_id=instance.id,
            actor="analyst",
            metadata={
                "status": instance.status,
                "assigned_to": instance.assigned_to,
            },
        )
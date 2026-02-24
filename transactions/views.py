from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.permissions import IsIngestService

from .serializers import TransactionIngestSerializer
from .models import Transaction
from audit.services import log_audit_event
from compliance.services import assess_transaction_risk


class TransactionIngestAPIView(APIView):
    permission_classes = [IsIngestService]
    """
    Internal endpoint for ingesting blockchain transactions.
    """

    def post(self, request):
        serializer = TransactionIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = serializer.save(status=Transaction.Status.RECEIVED)

        log_audit_event(
            event_type="TRANSACTION_INGESTED",
            entity_type="Transaction",
            entity_id=transaction.id,
            actor="system",
            metadata={
                "tx_hash": transaction.tx_hash,
                "blockchain": transaction.blockchain,
                "amount": str(transaction.amount),
                "asset": transaction.asset,
                "ingestion_source": transaction.ingestion_source,
            },
        )
        
        assessment = assess_transaction_risk(transaction)

        transaction.status = (
            Transaction.Status.FLAGGED
            if assessment.risk_level == "HIGH"
            else Transaction.Status.SCORED
        )
        transaction.save(update_fields=["status"])
        
        log_audit_event(
            event_type="TRANSACTION_RISK_SCORED",
            entity_type="RiskAssessment",
            entity_id=assessment.id,
            actor="system",
            metadata={
                "risk_score": assessment.risk_score,
                "risk_level": assessment.risk_level,
                "triggered_rules": assessment.triggered_rules,
            },
        )
        
        if assessment.risk_level == "HIGH":
            log_audit_event(
                event_type="COMPLIANCE_CASE_CREATED",
                entity_type="ComplianceCase",
                entity_id=transaction.compliance_case.id,
                actor="system",
                metadata={
                    "transaction_id": str(transaction.id),
                    "risk_score": assessment.risk_score,
                },
            )

        return Response(
            {
                "id": transaction.id,
                "status": transaction.status,
            },
            status=status.HTTP_201_CREATED,
        )
from django.db import models

# Create your models here.
import uuid
from django.db import models
from transactions.models import Transaction


class RiskAssessment(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="risk_assessment",
    )

    risk_score = models.IntegerField()
    risk_level = models.CharField(
        max_length=8,
        choices=RiskLevel.choices,
    )

    triggered_rules = models.JSONField()

    assessed_at = models.DateTimeField(auto_now_add=True)
    assessed_by = models.CharField(max_length=64, default="system")

    def __str__(self):
        return f"RiskAssessment({self.transaction_id}, {self.risk_level})"
    
    
class ComplianceCase(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="compliance_case",
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.OPEN,
    )

    assigned_to = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Compliance analyst identifier",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ComplianceCase({self.transaction_id}, {self.status})"
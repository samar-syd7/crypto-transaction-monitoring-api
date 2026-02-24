from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Transaction(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "RECEIVED", "Received"
        VALIDATED = "VALIDATED", "Validated"
        SCORED = "SCORED", "Scored"
        FLAGGED = "FLAGGED", "Flagged"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tx_hash = models.CharField(max_length=128)
    blockchain = models.CharField(max_length=32)

    from_address = models.CharField(max_length=256)
    to_address = models.CharField(max_length=256)

    amount = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        validators=[MinValueValidator(0)]
    )

    asset = models.CharField(max_length=16)

    block_number = models.BigIntegerField(null=True, blank=True)
    tx_timestamp = models.DateTimeField()

    ingestion_source = models.CharField(max_length=64)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.RECEIVED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tx_hash", "blockchain"],
                name="unique_tx_per_blockchain"
            )
        ]
        indexes = [
            models.Index(fields=["tx_hash"]),
            models.Index(fields=["from_address"]),
            models.Index(fields=["to_address"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.blockchain}:{self.tx_hash}"
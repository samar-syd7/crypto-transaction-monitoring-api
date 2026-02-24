from rest_framework import serializers
from .models import ComplianceCase


class ComplianceCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceCase
        fields = [
            "id",
            "transaction",
            "status",
            "assigned_to",
            "notes",
            "created_at",
            "closed_at",
        ]
        read_only_fields = ["id", "created_at", "closed_at", "transaction"]
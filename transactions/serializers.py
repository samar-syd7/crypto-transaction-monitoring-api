from rest_framework import serializers
from .models import Transaction


class TransactionIngestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "tx_hash",
            "blockchain",
            "from_address",
            "to_address",
            "amount",
            "asset",
            "block_number",
            "tx_timestamp",
            "ingestion_source",
        ]

    def validate_blockchain(self, value):
        return value.upper()

    def validate_asset(self, value):
        return value.upper()

    def validate(self, attrs):
        if attrs["from_address"] == attrs["to_address"]:
            raise serializers.ValidationError(
                "from_address and to_address cannot be the same"
            )
        return attrs
from rest_framework.test import APITestCase
from rest_framework import status
from config.jwt_utils import issue_service_token
from transactions.models import Transaction


class TransactionIngestionTest(APITestCase):

    def setUp(self):
        self.token = issue_service_token(
            role="INGEST_SERVICE",
            service_name="test_ingest_service"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_transaction_ingestion_success(self):
        payload = {
            "tx_hash": "0xtest_ingest_001",
            "blockchain": "eth",
            "from_address": "0xfrom",
            "to_address": "0xto",
            "amount": "15000",
            "asset": "USDT",
            "block_number": 123456,
            "tx_timestamp": "2025-01-01T12:00:00Z",
            "ingestion_source": "test_ingest_service",
        }

        response = self.client.post(
            "/api/transactions/ingest/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().status, "FLAGGED")
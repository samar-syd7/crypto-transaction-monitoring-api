from rest_framework.test import APITestCase
from config.jwt_utils import issue_service_token
from compliance.models import ComplianceCase
from rest_framework import status


class ComplianceCaseTest(APITestCase):

    def setUp(self):
        self.token = issue_service_token(
            role="INGEST_SERVICE",
            service_name="test_ingest_service"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_compliance_case_created_for_high_risk(self):
        payload = {
            "tx_hash": "0xhighrisk_case_001",
            "blockchain": "eth",
            "from_address": "0xfrom",
            "to_address": "0xto",
            "amount": "20000",
            "asset": "USDT",
            "block_number": 999999,
            "tx_timestamp": "2025-01-01T12:00:00Z",
            "ingestion_source": "test_ingest_service",
        }

        self.client.post("/api/transactions/ingest/", payload, format="json")

        self.assertEqual(ComplianceCase.objects.count(), 1)
        self.assertEqual(ComplianceCase.objects.first().status, "OPEN")


class ComplianceAnalystAccessTest(APITestCase):

    def setUp(self):
        self.token = issue_service_token(
            role="COMPLIANCE_ANALYST",
            service_name="test_compliance_dashboard"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_list_compliance_cases_authorized(self):
        response = self.client.get("/api/compliance/cases/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
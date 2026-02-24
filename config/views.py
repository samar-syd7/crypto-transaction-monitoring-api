from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .jwt_utils import issue_service_token


class IssueTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get("role")
        service_name = request.data.get("service_name")

        if role not in {"INGEST_SERVICE", "COMPLIANCE_ANALYST"}:
            return Response({"error": "Invalid role"}, status=400)

        if not service_name:
            return Response({"error": "service_name is required"}, status=400)

        token = issue_service_token(
            role=role,
            service_name=service_name,
        )

        return Response({"access": token})
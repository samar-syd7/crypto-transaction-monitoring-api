from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, "token"):
            return False

        role = request.user.token.get("role")
        return role == self.required_role


class IsIngestService(HasRole):
    required_role = "INGEST_SERVICE"


class IsComplianceAnalyst(HasRole):
    required_role = "COMPLIANCE_ANALYST"
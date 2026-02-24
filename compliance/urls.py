from django.urls import path
from .views import (
    ComplianceCaseListAPIView,
    ComplianceCaseUpdateAPIView,
)

urlpatterns = [
    path("cases/", ComplianceCaseListAPIView.as_view(), name="compliance-case-list"),
    path(
        "cases/<uuid:pk>/",
        ComplianceCaseUpdateAPIView.as_view(),
        name="compliance-case-update",
    ),
]
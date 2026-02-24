from django.urls import path
from .views import TransactionIngestAPIView

urlpatterns = [
    path("ingest/", TransactionIngestAPIView.as_view(), name="transaction-ingest"),
]
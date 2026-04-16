from django.urls import path

from .views import DashboardView, MeView, VerificationHistoryView, VerificationRequestView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("verification/", VerificationRequestView.as_view(), name="verification"),
    path("verification/history/", VerificationHistoryView.as_view(), name="verification-history"),
]

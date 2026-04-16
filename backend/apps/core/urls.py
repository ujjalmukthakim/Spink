from django.urls import path

from .views import (
    AdminLogListView,
    AdminUserListView,
    BanControlView,
    CreditControlView,
    PendingVerificationsView,
    VerificationApprovalView,
)

urlpatterns = [
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("credit-control/", CreditControlView.as_view(), name="admin-credit-control"),
    path("ban-control/", BanControlView.as_view(), name="admin-ban-control"),
    path("logs/", AdminLogListView.as_view(), name="admin-logs"),
    path("verifications/", PendingVerificationsView.as_view(), name="admin-verifications"),
    path("verification-review/", VerificationApprovalView.as_view(), name="admin-verification-review"),
]

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Verification
from apps.accounts.permissions import IsPlatformAdmin
from apps.accounts.serializers import VerificationSerializer

from .models import AdminLog
from .serializers import (
    AdminLogSerializer,
    AdminUserSerializer,
    BanControlSerializer,
    CreditControlSerializer,
    VerificationReviewSerializer,
)

User = get_user_model()


def log_action(admin_user, action, target_user=None, details=None):
    AdminLog.objects.create(
        admin_user=admin_user,
        target_user=target_user,
        action=action,
        details=details or {},
    )


class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsPlatformAdmin]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by("-date_joined")
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset


class CreditControlView(APIView):
    permission_classes = [IsPlatformAdmin]

    def post(self, request):
        serializer = CreditControlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, id=data["user_id"])
        old_credits = user.credits
        user.credits = data["credits"]
        user.save(update_fields=["credits"])
        log_action(
            request.user,
            "credit_update",
            user,
            {"old_credits": old_credits, "new_credits": data["credits"], "reason": data["reason"]},
        )
        return Response({"message": "Credits updated successfully."})


class BanControlView(APIView):
    permission_classes = [IsPlatformAdmin]

    def post(self, request):
        serializer = BanControlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, id=data["user_id"])
        user.is_banned = data["is_banned"]
        user.save(update_fields=["is_banned"])
        log_action(
            request.user,
            "ban_update",
            user,
            {"is_banned": data["is_banned"], "reason": data["reason"]},
        )
        return Response({"message": "User status updated successfully."})


class VerificationApprovalView(APIView):
    permission_classes = [IsPlatformAdmin]

    @transaction.atomic
    def post(self, request):
        serializer = VerificationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        verification = get_object_or_404(
            Verification.objects.select_for_update().select_related("user"),
            id=data["verification_id"],
        )
        verification.status = Verification.Status.APPROVED if data["approve"] else Verification.Status.REJECTED
        verification.reviewed_by = request.user
        verification.reviewed_at = timezone.now()
        verification.save(update_fields=["status", "reviewed_by", "reviewed_at"])
        verification.user.is_verified = data["approve"]
        verification.user.instagram_username = verification.instagram_username
        verification.user.save(update_fields=["is_verified", "instagram_username"])
        log_action(
            request.user,
            "verification_review",
            verification.user,
            {"verification_id": verification.id, "approved": data["approve"]},
        )
        return Response(VerificationSerializer(verification).data)


class PendingVerificationsView(generics.ListAPIView):
    permission_classes = [IsPlatformAdmin]
    serializer_class = VerificationSerializer

    def get_queryset(self):
        return Verification.objects.select_related("user").filter(status=Verification.Status.PENDING)


class AdminLogListView(generics.ListAPIView):
    permission_classes = [IsPlatformAdmin]
    serializer_class = AdminLogSerializer
    queryset = AdminLog.objects.select_related("admin_user", "target_user").all()

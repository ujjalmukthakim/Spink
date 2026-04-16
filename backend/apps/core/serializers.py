from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.serializers import UserSerializer, VerificationSerializer

from .models import AdminLog

User = get_user_model()


class AdminUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        read_only_fields = ()


class CreditControlSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    credits = serializers.IntegerField(min_value=0)
    reason = serializers.CharField(max_length=255)


class BanControlSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    is_banned = serializers.BooleanField()
    reason = serializers.CharField(max_length=255)


class VerificationReviewSerializer(serializers.Serializer):
    verification_id = serializers.IntegerField()
    approve = serializers.BooleanField()


class AdminLogSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source="admin_user.username", read_only=True)
    target_username = serializers.CharField(source="target_user.username", read_only=True)

    class Meta:
        model = AdminLog
        fields = ("id", "admin_username", "target_username", "action", "details", "created_at")

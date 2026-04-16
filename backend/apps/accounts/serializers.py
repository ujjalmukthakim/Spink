from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Verification

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "instagram_username",
            "credits",
            "trust_score",
            "is_verified",
            "is_admin",
            "is_banned",
        )
        read_only_fields = ("credits", "trust_score", "is_verified", "is_admin", "is_banned")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "instagram_username")

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            instagram_username=validated_data.get("instagram_username", ""),
        )


class RealLikeTokenSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_banned:
            raise serializers.ValidationError("Your account has been banned.")
        data["user"] = UserSerializer(self.user).data
        return data


class VerificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Verification
        fields = (
            "id",
            "user_username",
            "instagram_username",
            "verification_code",
            "status",
            "created_at",
            "reviewed_at",
        )
        read_only_fields = ("verification_code", "status", "created_at", "reviewed_at")


class VerificationRequestSerializer(serializers.Serializer):
    instagram_username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = self.context["request"].user
        user.instagram_username = validated_data["instagram_username"]
        user.save(update_fields=["instagram_username"])
        return Verification.objects.create(user=user, instagram_username=validated_data["instagram_username"])

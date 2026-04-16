from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "post_url",
            "owner",
            "owner_username",
            "required_likes",
            "current_likes",
            "status",
            "created_at",
        )
        read_only_fields = ("owner", "current_likes", "status", "created_at")

    def validate_post_url(self, value):
        if "instagram.com" not in value:
            raise serializers.ValidationError("Please submit a valid Instagram post URL.")
        return value

    def validate_required_likes(self, value):
        if value > 500:
            raise serializers.ValidationError("Required likes cannot exceed 500.")
        return value

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

from rest_framework import serializers

from apps.posts.serializers import PostSerializer

from .models import LikeTask


class LikeTaskSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = LikeTask
        fields = ("id", "post", "credit_delta", "trust_delta", "created_at")


class TaskConfirmSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

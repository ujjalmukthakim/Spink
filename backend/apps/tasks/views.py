from django.db import models
from django.db.models import Exists, OuterRef, F
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer

from .models import LikeTask
from .serializers import LikeTaskSerializer, TaskConfirmSerializer
from .services import confirm_like


class AvailableTaskListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        completed_subquery = LikeTask.objects.filter(
            user=user,
            post=OuterRef("pk")
        )

        return (
            Post.objects.select_related("owner")
            .annotate(already_done=Exists(completed_subquery))
            .filter(
                status=Post.Status.ACTIVE,
                owner__is_banned=False,
                current_likes__lt=F("required_likes"),
            )
            .exclude(owner=user)
            .filter(already_done=False)
            .order_by("-owner__trust_score", "created_at")
        )


class MyTaskHistoryView(generics.ListAPIView):
    serializer_class = LikeTaskSerializer

    def get_queryset(self):
        return LikeTask.objects.select_related(
            "post", "post__owner"
        ).filter(user=self.request.user)


class ConfirmTaskView(APIView):
    def post(self, request):
        serializer = TaskConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = confirm_like(
            request.user,
            serializer.validated_data["post_id"]
        )

        return Response(
            LikeTaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )
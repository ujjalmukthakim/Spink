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
from django.db import transaction
from django.db.models import F

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



def confirm_like(user, post_id):
    post = Post.objects.get(id=post_id)

    if user.credits < 1:
        raise ValueError("Not enough credits")

    with transaction.atomic():
        # create task
        task = LikeTask.objects.create(
            user=user,
            post=post,
            credit_delta=1
        )

        # 🔥 THIS IS THE MISSING PART
        user.credits = F("credits") - 1
        user.save(update_fields=["credits"])

        # (optional but important)
        post.current_likes = F("current_likes") + 1
        post.save(update_fields=["current_likes"])

    return task
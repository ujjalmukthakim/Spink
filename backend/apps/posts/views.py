from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related("owner").filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_verified:
            raise ValidationError("Verify your Instagram account before submitting posts.")
        serializer.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related("owner").filter(owner=self.request.user)

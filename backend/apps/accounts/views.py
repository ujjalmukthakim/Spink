from django.db.models import Sum
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.posts.models import Post
from apps.tasks.models import LikeTask

from rest_framework.permissions import IsAdminUser
from rest_framework import generics

from .models import Verification
from .serializers import (
    RealLikeTokenSerializer,
    RegisterSerializer,
    UserSerializer,
    VerificationRequestSerializer,
    VerificationSerializer,
)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = RealLikeTokenSerializer


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        pending_verification = Verification.objects.filter(
            user=user, status=Verification.Status.PENDING
        ).order_by("-created_at").first()

        return Response(
            {
                "user": UserSerializer(user).data,
                "stats": {
                    "submitted_posts": Post.objects.filter(owner=user).count(),
                    "active_posts": Post.objects.filter(owner=user, status=Post.Status.ACTIVE).count(),
                    "likes_given": LikeTask.objects.filter(user=user).count(),
                    "likes_received": LikeTask.objects.filter(post__owner=user).count(),
                    "credits_spent": LikeTask.objects.filter(post__owner=user).aggregate(total=Sum("credit_delta"))["total"] or 0,
                },
                "pending_verification": VerificationSerializer(pending_verification).data if pending_verification else None,
            }
        )


class VerificationRequestView(generics.CreateAPIView):
    serializer_class = VerificationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification = serializer.save()
        return Response(VerificationSerializer(verification).data, status=status.HTTP_201_CREATED)


class VerificationHistoryView(generics.ListAPIView):
    serializer_class = VerificationSerializer

    def get_queryset(self):
        return Verification.objects.filter(user=self.request.user).order_by("-created_at")
    
class AdminVerificationListView(generics.ListAPIView):
    serializer_class = VerificationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Verification.objects.filter(
            status=Verification.Status.PENDING
        ).order_by("-created_at")

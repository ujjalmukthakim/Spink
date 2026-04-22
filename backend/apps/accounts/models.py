import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_ref_code():
    return str(uuid.uuid4())[:8]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    instagram_username = models.CharField(max_length=150, blank=True)
    credits = models.PositiveIntegerField(default=0)
    trust_score = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    last_task_completed_at = models.DateTimeField(null=True, blank=True)
    referral_code = models.CharField(max_length=20,default=generate_ref_code)

    referred_by = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="referrals"
    )

    referral_rewarded = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Verification(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verifications")
    instagram_username = models.CharField(max_length=150)
    verification_code = models.CharField(max_length=32, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_verifications",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.status}"






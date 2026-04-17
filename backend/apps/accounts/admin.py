from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Verification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "username", "credits", "is_verified", "is_admin", "is_banned")
    list_editable = ("is_verified", "is_banned")  # 👈 ADD THIS

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "RealLike",
            {
                "fields": (
                    "instagram_username",
                    "credits",
                    "trust_score",
                    "is_verified",
                    "is_admin",
                    "is_banned",
                    "last_task_completed_at",
                )
            },
        ),
    )


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "instagram_username", "verification_code", "status", "created_at")

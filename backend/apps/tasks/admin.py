from django.contrib import admin

from .models import LikeTask


@admin.register(LikeTask)
class LikeTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "credit_delta", "created_at")

from django.conf import settings
from django.db import models

from apps.posts.models import Post


class LikeTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="like_tasks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_tasks")
    credit_delta = models.IntegerField(default=1)
    trust_delta = models.DecimalField(max_digits=4, decimal_places=2, default=0.02)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "post")
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["post", "created_at"]),
        ]

    def __str__(self):
        return f"{self.user} -> {self.post_id}"

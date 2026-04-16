from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.posts.models import Post

from .models import LikeTask

MIN_DELAY_SECONDS = 5
MAX_LIKES_PER_DAY = 100
TRUST_REWARD = Decimal("0.02")
TRUST_PENALTY = Decimal("0.10")
MAX_TRUST = Decimal("5.00")
MIN_TRUST = Decimal("0.10")


def clamp_trust(value):
    return max(MIN_TRUST, min(MAX_TRUST, value))


@transaction.atomic
def confirm_like(user, post_id):
    now = timezone.now()
    today = now.date()

    if user.is_banned:
        raise ValidationError("Banned users cannot complete tasks.")

    likes_today = LikeTask.objects.select_for_update().filter(user=user, created_at__date=today).count()
    if likes_today >= MAX_LIKES_PER_DAY:
        raise ValidationError("Daily like limit reached.")

    if user.last_task_completed_at and now - user.last_task_completed_at < timedelta(seconds=MIN_DELAY_SECONDS):
        user.trust_score = clamp_trust(user.trust_score - TRUST_PENALTY)
        user.save(update_fields=["trust_score"])
        raise ValidationError(f"Please wait at least {MIN_DELAY_SECONDS} seconds between tasks.")

    post = Post.objects.select_for_update().select_related("owner").filter(
        id=post_id, status=Post.Status.ACTIVE
    ).first()
    if not post:
        raise ValidationError("Task is no longer available.")

    if post.owner_id == user.id:
        raise ValidationError("You cannot like your own post.")

    if post.owner.credits < 1:
        raise ValidationError("Post owner has no credits remaining.")

    if post.current_likes >= post.required_likes:
        post.status = Post.Status.COMPLETED
        post.save(update_fields=["status"])
        raise ValidationError("Task has already been completed.")

    if LikeTask.objects.filter(user=user, post=post).exists():
        raise ValidationError("You already completed this task.")

    task = LikeTask.objects.create(user=user, post=post)

    user.__class__.objects.filter(id=user.id).update(
        credits=F("credits") + 1,
        trust_score=clamp_trust(user.trust_score + TRUST_REWARD),
        last_task_completed_at=now,
    )
    post.owner.__class__.objects.filter(id=post.owner_id).update(credits=F("credits") - 1)
    Post.objects.filter(id=post.id).update(current_likes=F("current_likes") + 1)

    post.refresh_from_db(fields=["current_likes", "required_likes", "status"])
    if post.current_likes >= post.required_likes and post.status != Post.Status.COMPLETED:
        post.status = Post.Status.COMPLETED
        post.save(update_fields=["status"])

    return task

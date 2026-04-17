from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the platform admin from environment variables."

    def handle(self, *args, **options):
        import os

        email = os.getenv("ADMIN_EMAIL")
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        if not all([email, username, password]):
            self.stdout.write(self.style.WARNING("Admin env vars are not fully configured."))
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": username, "is_staff": True, "is_superuser": True},
        )
        user.username = username
        user.is_admin = True
        user.is_staff = True
        # "is_verified": false,
        user.is_verified= True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Admin user {action}: {email}"))

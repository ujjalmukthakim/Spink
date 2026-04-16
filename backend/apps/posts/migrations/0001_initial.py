import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("post_url", models.URLField(unique=True)),
                ("required_likes", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("current_likes", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(choices=[("active", "Active"), ("completed", "Completed"), ("paused", "Paused")], default="active", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="posts", to="accounts.user")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["status", "created_at"], name="posts_post_status_2d848c_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["owner", "status"], name="posts_post_owner_i_587ef5_idx"),
        ),
    ]

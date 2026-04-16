from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LikeTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("credit_delta", models.IntegerField(default=1)),
                ("trust_delta", models.DecimalField(decimal_places=2, default=0.02, max_digits=4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("post", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="like_tasks", to="posts.post")),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="like_tasks", to="accounts.user")),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("user", "post")},
            },
        ),
        migrations.AddIndex(
            model_name="liketask",
            index=models.Index(fields=["user", "created_at"], name="tasks_liket_user_id_07b5ae_idx"),
        ),
        migrations.AddIndex(
            model_name="liketask",
            index=models.Index(fields=["post", "created_at"], name="tasks_liket_post_id_74b96e_idx"),
        ),
    ]

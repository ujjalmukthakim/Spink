from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=100)),
                ("details", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("admin_user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="admin_logs", to="accounts.user")),
                ("target_user", models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name="targeted_admin_logs", to="accounts.user")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]

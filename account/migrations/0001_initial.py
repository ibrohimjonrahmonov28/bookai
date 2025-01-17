# Generated by Django 4.2.1 on 2024-01-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("name", models.CharField(max_length=60, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email"
                    ),
                ),
                ("nickname", models.CharField(max_length=60, null=True, unique=True)),
                ("country", models.CharField(max_length=255, null=True)),
                ("date_birth", models.DateField(null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "male"), ("female", "female")],
                        max_length=6,
                        null=True,
                    ),
                ),
                ("phone_number", models.CharField(max_length=15, null=True)),
                ("password", models.CharField(max_length=500)),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("motto", models.TextField()),
                ("avatar", models.ImageField(upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("otp", models.CharField(max_length=6, null=True)),
                ("otp_max_try", models.IntegerField(default=3, null=True)),
                ("otp_expiry", models.DateTimeField(null=True)),
                ("otp_max_out", models.DateTimeField(null=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("writer", "writer"),
                            ("moderator", "moderator"),
                            ("user", "user"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

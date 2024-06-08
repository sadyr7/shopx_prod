# Generated by Django 5.0 on 2024-06-06 07:14

import app_userbase.validators
import app_userseller.usermanager
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategorySC",
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
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="SellerProfile",
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
                (
                    "email_or_phone",
                    models.CharField(blank=True, max_length=30, null=True, unique=True),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator("^\\+996\\d{9}$")
                        ],
                    ),
                ),
                (
                    "auth_token_refresh",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "auth_token_access",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Фамилия"
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=128,
                        validators=[app_userbase.validators.validate_password_strength],
                        verbose_name="password",
                    ),
                ),
                ("code", models.CharField(blank=True, max_length=6)),
                ("created_at", models.DateField(auto_now=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="usual/profiles/"
                    ),
                ),
                (
                    "device_token",
                    models.CharField(
                        max_length=100, verbose_name="токен от ios/android"
                    ),
                ),
                ("is_seller", models.BooleanField(default=False)),
                ("shop_name", models.CharField(max_length=255)),
                ("instagram_link", models.URLField(blank=True, null=True)),
                ("whatsapp_link", models.URLField(blank=True, null=True)),
                ("tiktok_link", models.URLField(blank=True, null=True)),
                ("facebook_link", models.URLField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продавец",
                "verbose_name_plural": "Продавец",
            },
            managers=[
                ("objects", app_userseller.usermanager.CustomUserManager()),
            ],
        ),
    ]

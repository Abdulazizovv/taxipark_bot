from typing import TYPE_CHECKING
from django.db import models


if TYPE_CHECKING:
    from botapp.models import BotUser


# Manager(admin) modeli
class Manager(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)

    role_choices = (
        ("admin", "Admin"),
        ("service", "Service"),
        ("user", "User"),
    )
    role = models.CharField(max_length=15, choices=role_choices, default="user")

    is_deleted = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    users: "models.QuerySet[BotUser]"

    def __str__(self):
        return self.full_name

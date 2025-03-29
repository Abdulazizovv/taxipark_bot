from typing import TYPE_CHECKING
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from botapp.models import BotUser

class ActiveManagerManager(models.Manager):
    """Custom Manager to filter out deleted managers."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted__isnull=True)

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

    objects = models.Manager()
    active_managers = ActiveManagerManager()  # Custom manager
    
    def __str__(self):
        return self.full_name

    
    def soft_delete(self):
        """Soft delete a manager instead of permanently removing them."""
        self.is_deleted = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted manager."""
        self.is_deleted = None
        self.save()


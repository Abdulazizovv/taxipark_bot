from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from manager.models import Manager


# Botga foydalanuvchilarini saqlash uchun model
class BotUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)

    full_name = models.CharField(max_length=255)

    username = models.CharField(max_length=255, null=True, blank=True)

    employee: "Manager | None" = models.ForeignKey(
        "manager.Manager", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="users"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Bot foydalanuvchisi"
        verbose_name_plural = "Bot foydalanuvchilari"
        ordering = ["-created_at"]

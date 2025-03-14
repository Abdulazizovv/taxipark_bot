from django.db import models
from django.core.exceptions import ValidationError


# Botga foydalanuvchilarini saqlash uchun model
class BotUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)
    phone_number = models.CharField(max_length=15)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)

    # Foydalanuvchini admin yoki servisdan biri ekanligini tekshirish
    def clean(self):
        if self.is_admin and self.is_service:
            raise ValidationError("A user cannot be both an admin and a service user.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Bot foydalanuvchisi'
        verbose_name_plural = 'Bot foydalanuvchilari'
        ordering = ['-created_at']
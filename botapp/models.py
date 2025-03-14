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
    role_choices = (
        ('admin', 'Admin'),
        ('service', 'Service'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=15, choices=role_choices, default='user') 

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Bot foydalanuvchisi'
        verbose_name_plural = 'Bot foydalanuvchilari'
        ordering = ['-created_at']
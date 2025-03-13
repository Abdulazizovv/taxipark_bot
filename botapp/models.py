from django.db import models


# Botga foydalanuvchilarini saqlash uchun model
class BotUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
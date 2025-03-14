from django.db import models


# Manager(admin) modeli
class Manager(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    is_deleted = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
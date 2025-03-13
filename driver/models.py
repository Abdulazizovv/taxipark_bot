from django.db import models


# Haydovchilar modeli
class Driver(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_color = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

from django.db import models


# Haydovchilar modeli
class Driver(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    def save(self):
        self.car_plate = self.car_plate.upper()
        super(Driver, self).save()

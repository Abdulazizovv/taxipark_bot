from django.db import models


# Haydovchilar modeli
class Driver(models.Model):
    phone_number = models.CharField(max_length=25, unique=True)
    full_name = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=10, unique=True)
    tariff_choices = (
        ("Standard", "Standard"),
        ("Comfort", "Comfort"),
        ("Business", "Business"),
        ("Premium", "Premium"),
    )
    tariff = models.CharField(max_length=10, choices=tariff_choices, default="Standard")
    balance = models.BigIntegerField(default=0)
    is_deleted = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    def save(self, **kwargs):
        self.full_name = self.full_name.title()
        self.car_model = self.car_model.title()
        self.car_plate = self.car_plate.upper()
        super(Driver, self).save(**kwargs)

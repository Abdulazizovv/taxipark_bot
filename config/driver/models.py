from django.db import models
from django.utils import timezone

# Haydovchilar modeli
class ActiveDriverManager(models.Manager):
    """Custom Manager to filter out deleted drivers."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted__isnull=True)

class Driver(models.Model):
    phone_number = models.CharField(max_length=25, unique=True)
    full_name = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=10, unique=True)
    
    TARIFF_CHOICES = (
        ("Standard", "Standard"),
        ("Comfort", "Comfort"),
        ("Business", "Business"),
        ("Premium", "Premium"),
    )
    tariff = models.CharField(max_length=10, choices=TARIFF_CHOICES, default="Standard")
    balance = models.BigIntegerField(default=0)

    is_deleted = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # Default manager
    active_drivers = ActiveDriverManager()  # Custom manager

    def __str__(self):
        return f"{self.full_name} - {self.car_plate}"

    def save(self, *args, **kwargs):
        """Ensure proper formatting before saving."""
        if self.full_name:
            self.full_name = self.full_name.title()
        if self.car_model:
            self.car_model = self.car_model.title()
        if self.car_plate:
            self.car_plate = self.car_plate.upper()
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Soft delete a driver instead of permanently removing them."""
        self.is_deleted = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted driver."""
        self.is_deleted = None
        self.save()

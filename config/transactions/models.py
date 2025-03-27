from django.db import models
from datetime import datetime
from django.utils import timezone

class Transaction(models.Model):
    driver = models.ForeignKey('driver.Driver', on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.driver} - {self.amount}'
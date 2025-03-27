from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from driver.models import Driver
import logging


@receiver(post_save, sender=Transaction)
def update_driver_balance(sender, instance, created, **kwargs):
    if created:
        try:
            driver = Driver.objects.get(id=instance.driver.id)
            driver.balance += instance.amount
            driver.save()
            logging.info(f"Driver {driver.id} balance updated to {driver.balance}")
        except Driver.DoesNotExist:
            pass
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BotUser
from manager.models import Manager


@receiver(post_save, sender=BotUser)
def check_user_is_admin(sender, instance, created, **kwargs):
    if created:
        if instance.phone_number in Manager.objects.values_list("phone_number", flat=True):
            instance.role = 'admin'
        

        
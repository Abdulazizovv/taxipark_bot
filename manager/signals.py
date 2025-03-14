from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Manager
from botapp.models import BotUser


# Manager qo'shilganda yoki o'zgartirilganida BotUser ni ham o'zgartirish uchun signal
@receiver(post_save, sender=Manager)
def toggle_bot_user_status(sender, instance, created, **kwargs):
    if created:
        if not instance.is_deleted:
            BotUser.objects.filter(phone_number=instance.phone_number).update(is_admin=True)
    else:
        if instance.is_deleted:
            BotUser.objects.filter(phone_number=instance.phone_number).update(is_admin=False)
        else:
            BotUser.objects.filter(phone_number=instance.phone_number).update(is_admin=True)


# Manager o'chirilgan BotUserni ham managerlikdan chiqarish uchun signal
@receiver(post_delete, sender=Manager)
def delete_manager(sender, instance, **kwargs):
    BotUser.objects.filter(phone_number=instance.phone_number).update(is_admin=False)
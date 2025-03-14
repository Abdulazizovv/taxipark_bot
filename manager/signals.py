from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Manager
from botapp.models import BotUser


# Manager qo'shilganda yoki o'zgartirilganida BotUser ni ham o'zgartirish uchun signal
# @receiver(post_save, sender=Manager)
# def change_bot_user_type(sender, instance, created, **kwargs):
#     if created:
#         # Agar yangi admin yaratilsa shu raqamli foydalanuvchini admin qilib belgilash
#         BotUser.objects.filter(phone_number=instance.phone_number).update(role='admin')
#     else:
#         if instance.is_deleted:
#             # Agar admin o'chirilsa shu raqamli foydalanuvchini oddiy foydalanuvchi qilib belgilash
#             BotUser.objects.filter(phone_number=instance.phone_number).update(role='user')
#         else:
#             # Agar adminni tahrirlasa shu raqamli foydalanuvchini admin qilib belgilash
#             BotUser.objects.filter(phone_number=instance.phone_number).update(role='admin')
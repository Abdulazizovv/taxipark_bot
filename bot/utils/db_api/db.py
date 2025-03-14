from asgiref.sync import sync_to_async
from botapp.models import BotUser
import logging


class DBCommands:
    # yangi user yaratish yoki userni olish
    @sync_to_async
    def get_or_create_user(self, user_id, phone_number: str|None, username: str|None, first_name: str, last_name: str|None):
        response = {}
        user, created = BotUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                'phone_number': phone_number,
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            logging.info(f"New user created: {user_id}")

        response = {
            'user': {
                'user_id': user.user_id,
                'phone_number': user.phone_number,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'created': created
        }
        return response
    

    @sync_to_async
    def bot_user_role(self, user_id):
        user = BotUser.objects.filter(user_id=user_id).first()
        if user:
            return user.role
        return None
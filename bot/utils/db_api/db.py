from asgiref.sync import sync_to_async
from botapp.models import BotUser
from manager.models import Manager
from driver.models import Driver
import logging


class DBCommands:
    # yangi user yaratish yoki userni olish
    @sync_to_async
    def get_or_create_bot_user(
        self, user_id: int, full_name: str, username: str = None
    ):
        response = {}
        user, created = BotUser.objects.get_or_create(
            user_id=user_id,
            defaults={"full_name": full_name, "username": username},
        )
        response["user"] = user
        response["created"] = created
        return response

    @sync_to_async
    def connect_user_to_employee(self, user_id: int, phone_number: str):
        try:
            employee = Manager.objects.get(phone_number=phone_number)
            user = BotUser.objects.get(user_id=user_id)
            user.employee = employee
            user.save()
            return True
        except Manager.DoesNotExist:
            logging.error(f"Manager with phone number {phone_number} does not exist")
            return False
        except BotUser.DoesNotExist:
            logging.error(f"User with id {user_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error connecting user to employee: {e}")
            return False

    @sync_to_async
    def get_employee_role(self, user_id: int):
        try:
            user = BotUser.objects.get(user_id=user_id)
            return user.employee.role
        except BotUser.DoesNotExist:
            logging.error(f"User with id {user_id} does not exist")
            return None
        except Exception as e:
            logging.error(f"Error getting employee: {e}")
            return None

    @sync_to_async
    def get_drivers_data(self, page: int = 1, page_size: int = 1):
        offset = (page - 1) * page_size
        return list(
            Driver.objects.values(
                "id", "full_name", "phone_number", "car_model", "car_plate", "balance"
            ).order_by("id")[
                offset : offset + page_size
            ]
        )
    

    @sync_to_async
    def get_driver(self, driver_id: int):
        try:
            driver = Driver.objects.filter(id=driver_id).values(
                "id", "full_name", "phone_number", "car_model", "car_plate", "balance"
            ).first()

            if driver:
                return driver
            else:
                logging.error(f"Driver with id {driver_id} does not exist")
                return None

        except Exception as e:
            logging.error(f"Error getting driver: {e}")
            return None

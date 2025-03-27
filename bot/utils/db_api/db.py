from asgiref.sync import sync_to_async
from botapp.models import BotUser
from manager.models import Manager
from driver.models import Driver
from service.models import Service
from service_category.models import ServiceCategory
from transactions.models import Transaction
import logging
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError


class DbResponse:
    def __init__(self, success: bool=False, message: str = None, data: dict = None):
        self.success = success
        self.message = message
        self.data = data
    

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
    def get_drivers_data(self):
        return list(
            Driver.objects.values(
                "id", "full_name", "phone_number", "car_model", "car_plate", "balance", "tariff"
            ).order_by("id")
        )
    

    @sync_to_async
    def search_drivers(self, search_query: str):
        return list(
            Driver.objects.filter(
                Q(full_name__icontains=search_query)
                | Q(phone_number__icontains=search_query)
                | Q(car_model__icontains=search_query)
                | Q(car_plate__icontains=search_query)
                | Q(tariff__icontains=search_query)
            )
            .values(
                "id", "full_name", "phone_number", "car_model", "car_plate", "balance", "tariff"
            )
            .order_by(Lower("full_name"))
        )
    
    @sync_to_async
    def check_phone_number_exists(self, phone_number: str):
        phone_number_exists = Driver.objects.filter(phone_number=phone_number).exists()
        if phone_number_exists:
            return DbResponse(success=False, message="Bu telefon raqam allaqachon ro'yxatdan o'tgan", data=None)
        return DbResponse(success=True, message="Telefon raqam bo'sh", data=None)
    
    @sync_to_async
    def check_car_plate(self, car_plate: str):
        car_plate_exists = Driver.objects.filter(car_plate=car_plate.upper()).exists()
        if car_plate_exists:
            return DbResponse(success=False, message="Bu avtomobil raqami allaqachon ro'yxatdan o'tgan", data=None)
        return DbResponse(success=True, message="Avtomobil raqami bo'sh", data=None)

    @sync_to_async
    def add_new_driver(
        self, full_name: str, phone_number: str, car_model: str, car_plate: str, tariff: str
    ):
        try:
            driver = Driver.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                car_model=car_model,
                car_plate=car_plate,
                tariff=tariff,
            )
            return DbResponse(success=True, message="Yangi haydovchi muvaffaqiyatli qo'shildi", data={"driver_id": driver.id})
        
        except ValidationError as e:
            print(e.message_dict)
            if "phone_number" in e.message_dict:
                logging.error(f"Phone number {phone_number} already exists")
                return DbResponse(success=False, message="Bu telefon raqam allaqachon ro'yxatdan o'tgan", data=None)
            if "car_plate" in e.message_dict:
                logging.error(f"Car plate {car_plate} already exists")
                return DbResponse(success=False, message="Bu avtomobil raqami allaqachon ro'yxatdan o'tgan", data=None)
            return DbResponse(success=False, message="Xatolik sodir bo'ldi", data=None)

        except Exception as e:
            logging.error(f"Error adding new driver: {e}")
            return DbResponse(success=False, message="Xatolik sodir bo'ldi", data=None)
    
    @sync_to_async
    def enought_driver_balance(self, driver_id: int, amount: int):
        try:
            driver = Driver.objects.get(id=driver_id)
            if driver.balance >= amount:
                return True
            return False
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error checking driver balance: {e}")
            return False


    @sync_to_async
    def get_driver(self, driver_id: int):
        try:
            driver = (
                Driver.objects.filter(id=driver_id)
                .values(
                    "id",
                    "full_name",
                    "phone_number",
                    "car_model",
                    "car_plate",
                    "balance",
                    "tariff",
                    "created_at",
                    "updated_at",
                )
                .first()
            )

            if driver:
                return DbResponse(success=True, message="Haydovchi ma'lumotlari", data=driver)
            else:
                logging.error(f"Driver with id {driver_id} does not exist")
                return DbResponse(success=False, message="Haydovchi topilmadi", data=None)
            

        except Exception as e:
            logging.error(f"Error getting driver: {e}")
            return DbResponse(success=False, message="Xatolik sodir bo'ldi", data=None)
        
    @sync_to_async
    def get_driver_by_car_plate(self, car_plate: str):
        try:
            driver = (
                Driver.objects.filter(car_plate=car_plate)
                .values(
                    "id",
                    "full_name",
                    "phone_number",
                    "car_model",
                    "car_plate",
                    "balance",
                    "tariff",
                )
                .first()
            )

            if driver:
                return driver
            else:
                logging.error(f"Driver with car plate {car_plate} does not exist")
                return None

        except Exception as e:
            logging.error(f"Error getting driver: {e}")
            return None
        
    @sync_to_async
    def delete_driver(self, driver_id: int):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.delete()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error deleting driver: {e}")
            return False
        
    @sync_to_async
    def edit_driver_full_name(self, driver_id: int, full_name: str):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.full_name = full_name
            driver.save()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error editing driver full name: {e}")
            return False
    

    @sync_to_async
    def edit_driver_phone_number(self, driver_id: int, phone_number: str):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.phone_number = phone_number
            driver.save()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error editing driver phone number: {e}")
            return False
    

    @sync_to_async
    def edit_driver_car_model(self, driver_id: int, car_model: str):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.car_model = car_model
            driver.save()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error editing driver car model: {e}")
            return False
    

    @sync_to_async
    def edit_driver_car_plate(self, driver_id: int, car_plate: str):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.car_plate = car_plate
            driver.save()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error editing driver car plate: {e}")
            return False
        
    @sync_to_async
    def edit_driver_tariff(self, driver_id: int, tariff: str):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.tariff = tariff
            driver.save()
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error editing driver tariff: {e}")
            return False

    
    @sync_to_async
    def add_balance(self, driver_id: int, amount: int, description: str|None = None):
        try:
            driver = Driver.objects.get(id=driver_id)
            Transaction.objects.create(driver=driver, amount=amount, description=description if description else "Admin tomondan balansni to'ldirish")
            logging.info(f"Balance added to driver with id {driver_id}")
            return True
        except Driver.DoesNotExist:
            logging.error(f"Driver with id {driver_id} does not exist")
            return False
        except Exception as e:
            logging.error(f"Error adding balance: {e}")
            return False
    
    #==================== Service Categories ====================

    @sync_to_async
    def get_service_category_by_name(self, name: str):
        try:
            category = ServiceCategory.objects.filter(name=name)
            if category.exists():
                data = {
                    "id": category.values().first()["id"],
                    "name": category.values().first()["name"],
                    "description": category.values().first()["description"],
                }
                return DbResponse(success=True, message="Servis kategoriya ma'lumotlari", data=data)
            else:
                return DbResponse(success=False, message="Servis kategoriya topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error getting service category: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
    
    @sync_to_async
    def get_all_category_services(self):
        data = list(
            ServiceCategory.objects.values(
                "id", "name", "description"
            ).order_by("id")
        )
        if data:
            return DbResponse(success=True, message="Servis kategoriyalari ro'yxati", data=data)
        else:
            return DbResponse(success=False, message="Servis kategoriyalari topilmadi", data=None)
        
    @sync_to_async
    def service_category_get_or_create(self, name: str):
        try:
            category, created = ServiceCategory.objects.get_or_create(name=name)
            return DbResponse(success=True, message="Servis kategoriya muvaffaqiyatli qo'shildi", data={"category_id": category.id, "created": created})
        except Exception as e:
            logging.error(f"Error creating service category: {e}")
            return DbResponse(success=False, message="Servis kategoriya qismida xatolik!", data=None)
        
    @sync_to_async
    def exclude_service_categories(self, category_ids: list):
        data = list(ServiceCategory.objects.exclude(id__in=category_ids).values("id", "name").order_by("id"))
        if data:
            return DbResponse(success=True, message="Servis kategoriyalari ro'yxati", data=data)
        else:
            return DbResponse(success=False, message="Servis kategoriyalari topilmadi", data=None)

    
    # ==================== Services ====================
    
    @sync_to_async
    def get_all_services(self):
        
        data = list(
            Service.objects.values(
                "id", "phone_number", "title", "description", "created_at", "updated_at"
            ).order_by("id")
        )
        if data:
            return DbResponse(success=True, message="Servislar ro'yxati", data=data)
        else:
            return DbResponse(success=False, message="Servislar topilmadi", data=None)
    

    @sync_to_async
    def create_new_service(self, title, description: str|None, phone_number: str, category_ids: list):
        try:
            service = Service.objects.create(title=title, description=description, phone_number=phone_number)
            service.category.set(category_ids)
            return DbResponse(success=True, message="Yangi servis muvaffaqiyatli qo'shildi", data={"service_id": service.id})
        except Exception as e:
            logging.error(f"Error creating new service: {e}")
            return DbResponse(success=False, message="Servis qo'shishda xatolik sodir bo'ldi", data=None)

    @sync_to_async
    def get_service_by_id(self, id: str):
        try:
            service = Service.objects.filter(id=id)
            if service.exists():
                data = {
                    "id": service.values().first()["id"],
                    "phone_number": service.values().first()["phone_number"],
                    "title": service.values().first()["title"],
                    "categories": [category.name for category in service.first().category.all()],
                    "description": service.values().first()["description"],
                    "created_at": service.values().first()["created_at"],
                    "updated_at": service.values().first()["updated_at"],
                }
                return DbResponse(success=True, message="Servis ma'lumotlari", data=data)
            else:
                return DbResponse(success=False, message="Servis topilmadi", data=None)
            

        except Exception as e:
            logging.error(f"Error getting service: {e}")
            return DbResponse(success=False, message="Xatolik sodir bo'ldi", data=None)


    @sync_to_async
    def get_service_by_title(self, title: str):
        try:
            service = Service.objects.filter(title=title)
            if service.exists():
                data = {
                    "id": service.values().first()["id"],
                    "phone_number": service.values().first()["phone_number"],
                    "title": service.values().first()["title"],
                    "categories": [category.name for category in service.first().category.all()],
                    "description": service.values().first()["description"],
                    "created_at": service.values().first()["created_at"],
                    "updated_at": service.values().first()["updated_at"],
                }
                return DbResponse(success=True, message="Servis ma'lumotlari", data=data)
            else:
                return DbResponse(success=False, message="Servis topilmadi", data=None)
            

        except Exception as e:
            logging.error(f"Error getting service: {e}")
            return DbResponse(success=False, message="Xatolik sodir bo'ldi", data=None)
    

    @sync_to_async
    def check_service_title_exists(self, title: str):
        title_exists = Service.objects.filter(title=title).exists()
        if title_exists:
            return DbResponse(success=False, message="Bu nom bilan servis allaqachon ro'yxatdan o'tgan! Boshqa nom kiriting.", data=None)
        return DbResponse(success=True, message="Servis nomi bo'sh", data=None)
    

    # ==================== Edit Service ====================

    @sync_to_async
    def delete_service(self, service_id: int):
        try:
            service = Service.objects.get(id=service_id)
            service.delete()
            return DbResponse(success=True, message="Servis muvaffaqiyatli o'chirildi", data=None)
        except Service.DoesNotExist:
            logging.error(f"Service with id {service_id} does not exist")
            return DbResponse(success=False, message="Servis topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error deleting service: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)


    @sync_to_async
    def edit_service_title(self, service_id: int, title: str):
        try:
            service = Service.objects.get(id=service_id)
            service.title = title
            service.save()
            return DbResponse(success=True, message="Servis nomi muvaffaqiyatli o'zgartirildi", data=None)
        except Service.DoesNotExist:
            logging.error(f"Service with id {service_id} does not exist")
            return DbResponse(success=False, message="Servis topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error editing service title: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
    

    @sync_to_async
    def edit_service_description(self, service_id: int, description: str):
        try:
            service = Service.objects.get(id=service_id)
            service.description = description
            service.save()
            return DbResponse(success=True, message="Servis haqida ma'lumot muvaffaqiyatli o'zgartirildi", data=None)
        except Service.DoesNotExist:
            logging.error(f"Service with id {service_id} does not exist")
            return DbResponse(success=False, message="Servis topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error editing service description: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
    

    @sync_to_async
    def edit_service_phone_number(self, service_id: int, phone_number: str):
        try:
            service = Service.objects.get(id=service_id)
            service.phone_number = phone_number
            service.save()
            return DbResponse(success=True, message="Servis telefon raqami muvaffaqiyatli o'zgartirildi", data=None)
        except Service.DoesNotExist:
            logging.error(f"Service with id {service_id} does not exist")
            return DbResponse(success=False, message="Servis topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error editing service phone number: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
        
    
    @sync_to_async
    def edit_service_category(self, service_id: int, category_ids: list):
        try:
            service = Service.objects.get(id=service_id)
            service.category.set(category_ids)
            return DbResponse(success=True, message="Servis kategoriyasi muvaffaqiyatli o'zgartirildi", data=None)
        except Service.DoesNotExist:
            logging.error(f"Service with id {service_id} does not exist")
            return DbResponse(success=False, message="Servis topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error editing service category: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
        
    
    # ==================== Get statistics ====================
    @sync_to_async
    def get_users_stats(self):
        all_users = BotUser.objects.count()
        connected_users = BotUser.objects.exclude(employee=None).count()
        manager_users = Manager.objects.filter(role="admin").count()
        service_users = Manager.objects.filter(role="service").count()
        return {
            "all_users": all_users,
            "connected_users": connected_users,
            "manager_users": manager_users,
            "service_users": service_users,
        }

    @sync_to_async
    def get_drivers_stats(self):
        drivers_count = Driver.objects.count()
        active_drivers = Driver.objects.filter(is_deleted=None).count()
        inactive_drivers = Driver.objects.exclude(is_deleted=None).count()
        return {
            "count": drivers_count,
            "active_drivers": active_drivers,
            "inactive_drivers": inactive_drivers,
        }
    
    @sync_to_async
    def get_services_stats(self):
        services_count = Service.objects.count()
        service_categories_count = ServiceCategory.objects.count()
        return {
            "count": services_count,
            "category_count": service_categories_count,
        }
    
    @sync_to_async
    def get_transactions_stats(self):
        transactions_count = Transaction.objects.count()
        return {
            "count": transactions_count,
        }

    @sync_to_async
    def get_drivers_count(self):
        return Driver.objects.count()
    
    @sync_to_async
    def get_services_count(self):
        return Service.objects.count()
    
    @sync_to_async
    def get_service_categories_count(self):
        return ServiceCategory.objects.count()
    
    @sync_to_async
    def get_transactions_count(self):
        return Transaction.objects.count()
    
    @sync_to_async
    def get_all_transactions(self):
        data = list(
            Transaction.objects.values(
                "id", "driver_id", "amount", "description", "created_at"
            ).order_by("id")
        )
        if data:
            return DbResponse(success=True, message="Tranzaksiyalar ro'yxati", data=data)
        return DbResponse(success=False, message="Tranzaksiyalar topilmadi", data=None)
    

    # ==================== Service Manager ====================
    @sync_to_async
    def get_user_services(self, user_id: str) -> DbResponse:
        try:
            user = BotUser.objects.get(user_id=user_id)
            services = user.employee.services.all()
            data = list(
                services.values(
                    "id", "phone_number", "title", "description", "created_at", "updated_at"
                ).order_by("id")
            )
            return DbResponse(success=True, message="Servislar ro'yxati", data=data)
        except BotUser.DoesNotExist:
            logging.error(f"User with id {user_id} does not exist")
            return DbResponse(success=False, message="Foydalanuvchi topilmadi", data=None)
        except Exception as e:
            logging.error(f"Error getting user services: {e}")
            return DbResponse(success=False, message="Noma'lum xatolik sodir bo'ldi", data=None)
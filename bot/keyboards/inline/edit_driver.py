from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_driver_detail_cb = CallbackData("edit_driver_detail", "driver_id", "action")

def edit_driver_info_kb(driver_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ism", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_full_name")),
                InlineKeyboardButton(text="Telefon raqam", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_phone_number")),
            ],
            [
                InlineKeyboardButton(text="Mashina modeli", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_car_model")),
                InlineKeyboardButton(text="Mashina raqami", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_car_plate")),
            ],
            [
                InlineKeyboardButton(text="Tarif", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_tariff")),
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="back")),
            ]
        ]
    )
    return kb
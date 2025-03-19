from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_driver_detail_cb = CallbackData("edit_driver_detail", "driver_id", "action")

def edit_driver_info_kb(driver_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ismni o'zgartirish", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_full_name")),
            ],
            [
                InlineKeyboardButton(text="Telefon raqamni o'zgartirish", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_phone_number")),
            ],
            [
                InlineKeyboardButton(text="Mashina modelini o'zgartirish", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_car_model")),
            ],
            [
                InlineKeyboardButton(text="Mashina raqamini o'zgartirish", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_car_plate")),
            ],
            [
                InlineKeyboardButton(text="Tarifni o'zgartirish", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="edit_tariff")),
            ],
            [
                InlineKeyboardButton(text="O'chirish🗑", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="delete")),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data=edit_driver_detail_cb.new(driver_id=driver_id, action="back")),
            ]
        ]
    )
    return kb
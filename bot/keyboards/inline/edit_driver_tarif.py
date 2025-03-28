from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_driver_tariff_cb = CallbackData("edit_driver_detail", "driver_id", "action")

def edit_driver_tariff_kb(driver_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Standard", callback_data=edit_driver_tariff_cb.new(driver_id=driver_id, action="standard")),
            ],
            [
                InlineKeyboardButton(text="Comfort", callback_data=edit_driver_tariff_cb.new(driver_id=driver_id, action="comfort")),
            ],
            [
                InlineKeyboardButton(text="Premuim", callback_data=edit_driver_tariff_cb.new(driver_id=driver_id, action="premium")),
            ],
            [
                InlineKeyboardButton(text="Business", callback_data=edit_driver_tariff_cb.new(driver_id=driver_id, action="business")),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data=edit_driver_tariff_cb.new(driver_id=driver_id, action="back")),
            ]
        ]
    )
    return kb
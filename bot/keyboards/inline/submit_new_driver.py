from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

submit_new_driver_cb = CallbackData("submit_new", "action")

def submit_new_driver_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Tasdiqlash✅",
                    callback_data=submit_new_driver_cb.new(action="submit")
                )
            ],
            [
                InlineKeyboardButton(
                    text="Bekor qilish❌",
                    callback_data=submit_new_driver_cb.new(action="cancel")
                )
            ]
        ]
    )
    return kb

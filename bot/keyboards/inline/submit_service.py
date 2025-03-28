from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


submit_service_cb = CallbackData("submit_service", "action")

def submit_service_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Bekor qilish❌",
                    callback_data=submit_service_cb.new(
                        action="cancel"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Tasdiqlash✅",
                    callback_data=submit_service_cb.new(
                        action="submit"
                    )
                )
            ],
        ]
    )
    return kb
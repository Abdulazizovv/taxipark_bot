from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

confirm_order_cb = CallbackData("confirm_order", "action", "driver_id", "service_id", "summa")

def confirm_order_kb(driver_id: int, service_id: int, summa: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Tasdiqlash 🟢",
                    callback_data=confirm_order_cb.new(action="confirm", driver_id=driver_id, service_id=service_id, summa=summa)
                ),
                InlineKeyboardButton(
                    text="Bekor qilish 🔴",
                    callback_data=confirm_order_cb.new(action="cancel", driver_id=driver_id, service_id=service_id, summa=summa)
                )
            ]
        ]
    )
    return kb

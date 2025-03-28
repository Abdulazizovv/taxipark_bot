from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

driver_detail_callback = CallbackData("edit_driver", "driver_id", "action")


def edit_driver_detail_kb(driver_id: int):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="O'zgartirish✏️", callback_data=driver_detail_callback.new(driver_id=driver_id, action="edit")),
                InlineKeyboardButton(text="O'chirish🗑", callback_data=driver_detail_callback.new(driver_id=driver_id, action="delete")),
            ],
            [
                InlineKeyboardButton(text="Balansni to'ldirish💰", callback_data=driver_detail_callback.new(driver_id=driver_id, action="add_balance")),
            ],
            [
                InlineKeyboardButton(text="Bosh menyu", callback_data="main_menu"),
            ]
        ]
    )
    return kb
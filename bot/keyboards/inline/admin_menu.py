from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

admin_menu_cd = CallbackData("admin_menu", "action")

admin_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Haydovchilar🚖", callback_data=admin_menu_cd.new(action="drivers")),
            InlineKeyboardButton(text="Yangi haydovchi➕", callback_data=admin_menu_cd.new(action="new_driver")),
        ],
        [
            InlineKeyboardButton(text="Servislar📍", callback_data=admin_menu_cd.new(action="seriveces")),
            InlineKeyboardButton(text="Yangi servis➕", callback_data=admin_menu_cd.new(action="new_service")),
        ],
    ]
)
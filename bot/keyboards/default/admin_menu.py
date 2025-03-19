from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Haydovchilar🚖"),
            KeyboardButton(text="Yangi haydovchi➕"),
        ],
        [
            KeyboardButton(text="Servislar📍"),
            KeyboardButton(text="Yangi servis➕"),
        ],
        [
            KeyboardButton(text="📊Statistika"),
        ],
    ],
    resize_keyboard=True,
)

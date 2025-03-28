from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


service_admin_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Xizmat ko'rsatish"),
            KeyboardButton(text="📊 Hisobotlar")
        ],
    ],
    resize_keyboard=True
)
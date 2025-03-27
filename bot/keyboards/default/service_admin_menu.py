from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


service_admin_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Xizmatlar"),
            KeyboardButton(text="📊 Hisobotlar")
        ],
        [
            KeyboardButton(text="📈 Statistika"),
        ]
    ],
    resize_keyboard=True
)
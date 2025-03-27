from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def select_service_category_keyboard(categories):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.insert(KeyboardButton(text="⬅️ Orqaga"))
    for category in categories:
        keyboard.add(KeyboardButton(text=category))
    return keyboard
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def select_service_keyboard(services):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(KeyboardButton("🔙 Orqaga"))
    for service in services:
        kb.add(KeyboardButton(service['title']))
    return kb
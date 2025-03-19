from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def service_category_add_kb(service_categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(KeyboardButton(text="⬅️Orqaga"))
    kb.insert(KeyboardButton(text="Davom etish▶️"))

    for category in service_categories:
        kb.add(KeyboardButton(text=category['name']))


    return kb
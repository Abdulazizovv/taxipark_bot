from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def service_category_kb(categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(*[KeyboardButton(category['name']) for category in categories])
    kb.add(KeyboardButton("⬅️Orqaga"))
    return kb

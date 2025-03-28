from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def services_kb(services):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    
    kb.add(*[KeyboardButton(service["title"]) for service in services])

    kb.add(KeyboardButton("⬅️Orqaga"))
    return kb
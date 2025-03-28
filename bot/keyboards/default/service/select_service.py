from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def select_service_keyboard(services):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    
    services_kb = [KeyboardButton(service["title"]) for service in services]
    
    kb.add(*services_kb)
    kb.add(KeyboardButton("🔙 Orqaga"))
    
    return kb
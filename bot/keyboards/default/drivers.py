from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def drivers_kb(drivers, page=1, has_next=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.insert(KeyboardButton(text="🔍Qidirish"))
    kb.insert(KeyboardButton(text="🔙Orqaga"))
    for driver in drivers:
        kb.add(KeyboardButton(text=driver["full_name"]))
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(KeyboardButton(text="⬅️"))
    if has_next:
        pagination_buttons.append(KeyboardButton(text="➡️"))
    if pagination_buttons:
        kb.row(*pagination_buttons)
    return kb

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)
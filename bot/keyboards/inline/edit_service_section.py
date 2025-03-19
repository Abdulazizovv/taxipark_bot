from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

edit_service_section_cb = CallbackData("edit_service_section", "section", "service_id")

def edit_service_section_kb(service_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Nomini tahrirlash", callback_data=edit_service_section_cb.new(section="name", service_id=service_id))
            ],
            [
                InlineKeyboardButton(text="Tavsifini tahrirlash", callback_data=edit_service_section_cb.new(section="description", service_id=service_id))
            ],
            [
                InlineKeyboardButton(text="Telefon raqamini tahrirlash", callback_data=edit_service_section_cb.new(section="phone", service_id=service_id))
            ]
        ]
    )
    return kb
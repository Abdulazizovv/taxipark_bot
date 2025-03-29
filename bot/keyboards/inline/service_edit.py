from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


service_edit_callback = CallbackData("service_edit", "action", "service_id")


def service_edit_kb(service_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Servisni tahrirlash✏️",
                callback_data=service_edit_callback.new(action="edit", service_id=service_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="Servisni o'chirish🗑",
                callback_data=service_edit_callback.new(action="delete", service_id=service_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="Menejerlar👥",
                callback_data=service_edit_callback.new(action="managers", service_id=service_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️Orqaga",
                callback_data=service_edit_callback.new(action="back", service_id=service_id)
            )
        ]
    ]
    )

    return kb
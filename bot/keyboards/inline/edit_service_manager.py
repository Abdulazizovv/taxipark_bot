from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


manager_edit_callback = CallbackData("manager_edit", "action", "manager_id", "service_id")


def manager_edit_kb(manager_id: int, service_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Menejerni tahrirlash✏️",
                callback_data=manager_edit_callback.new(action="edit", manager_id=manager_id, service_id=service_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="Menejerni o'chirish🗑",
                callback_data=manager_edit_callback.new(action="delete", manager_id=manager_id, service_id=service_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data=manager_edit_callback.new(action="back", manager_id=manager_id, service_id=service_id)
            )
        ]
    ]
    )

    return kb
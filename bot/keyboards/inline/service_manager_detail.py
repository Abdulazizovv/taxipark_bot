from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


service_manager_edit_cb = CallbackData("service_manager_edit", "action", "manager_id", "service_id")


def service_manager_edit_kb(manager_id: int, service_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ism 👤", callback_data=service_manager_edit_cb.new(action="name", manager_id=manager_id, service_id=service_id)),
                InlineKeyboardButton(text="Telefon raqam 📞", callback_data=service_manager_edit_cb.new(action="phone_number", manager_id=manager_id, service_id=service_id)),
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=service_manager_edit_cb.new(action="back", manager_id=manager_id, service_id=service_id)),
            ]
        ]
    )

    return kb
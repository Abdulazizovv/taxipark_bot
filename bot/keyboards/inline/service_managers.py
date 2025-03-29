from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


select_manager_callback = CallbackData("select_manager", "manager_id", "service_id")


def select_manager_kb(managers: list[dict], service_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.insert(InlineKeyboardButton(text="Yangi menejer qo'shish ➕", callback_data=select_manager_callback.new(manager_id=0, service_id=service_id)))
    for manager in managers:
        kb.add(
            InlineKeyboardButton(
                text=f"{manager['full_name']} | {manager['phone_number']}",
                callback_data=select_manager_callback.new(manager_id=manager["id"], service_id=service_id),
            )
        )
    kb.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=select_manager_callback.new(manager_id=-1, service_id=service_id)))
    return kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pagination_keyboard(service_id: int, current_page: int, total_pages: int):
    keyboard = InlineKeyboardMarkup(row_width=2)

    if current_page > 1:
        keyboard.insert(
            InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"transactions:{service_id}:{current_page - 1}",
            )
        )

    keyboard.insert(
        InlineKeyboardButton(
            text=f"📄 {current_page}/{total_pages}", callback_data="ignore"
        )
    )

    if current_page < total_pages:
        keyboard.insert(
            InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"transactions:{service_id}:{current_page + 1}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text="📥 Excel Yuklash", callback_data=f"download:transactions:{service_id}"
        )
    )
    keyboard.add(InlineKeyboardButton(
        text="🔙 Orqaga",
        callback_data="back:transactions"
    ))

    return keyboard

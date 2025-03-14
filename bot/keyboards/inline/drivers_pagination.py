from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

driver_cd = CallbackData("driver", "driver_id")
drivers_pagination_cd = CallbackData("drivers_pagination", "page")


def drivers_pagination_kb(drivers, page: int=1):
    kb = InlineKeyboardMarkup(row_width=1)
    for driver in drivers:
        kb.insert(
            InlineKeyboardButton(
                text=driver['full_name'],
                callback_data=driver_cd.new(
                    driver_id=driver['id']
                )
            )
        )

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=drivers_pagination_cd.new(
                    page=page - 1
                )
            )
        )

    if len(drivers) == 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=drivers_pagination_cd.new(
                    page=page + 1
                )
            )
        )
    
    
    if pagination_buttons:
        kb.row(*pagination_buttons)
    
    kb.add(
        InlineKeyboardButton(
            text="🔙",
            callback_data="main_menu"
        )
    )
    
    return kb
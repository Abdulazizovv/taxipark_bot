from aiogram import types
from bot.loader import dp, db
from bot.filters import IsAdmin
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot.utils.main import format_currency


@dp.message_handler(IsAdmin(), text="Haydovchilar🚖")
async def show_drivers(message: types.Message):
    await message.answer(
        "Haydovchilar",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Qidirish", switch_inline_query_current_chat=""
                    )
                ]
            ]
        ),
    )


@dp.inline_handler(IsAdmin(), state="*")
async def inline_search(query: types.InlineQuery):
    text = query.query.strip()
    
    offset = int(query.offset) if query.offset else 0
    limit = 50  # Telegram allows up to 50 results

    if not text:
        drivers = await db.get_drivers_data(limit=limit, offset=offset)
    else:
        drivers = await db.search_drivers(text, limit=limit, offset=offset)

    results = []

    for driver in drivers:
        results.append(
            InlineQueryResultArticle(
                id=str(driver["id"]),
                title=driver["full_name"],
                description=f"{driver['phone_number']}\n{driver['car_model']} - {driver['car_plate']}\nTarif: {driver['tariff']}\nBalans: {format_currency(int(driver['balance']))}",
                input_message_content=InputTextMessageContent(
                    message_text=f"🚖 {driver['car_plate']}"
                ),
            )
        )

    next_offset = str(offset + limit) if len(drivers) == limit else ""

    await query.answer(results, cache_time=1, next_offset=next_offset)  # Add pagination



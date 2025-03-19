from aiogram import types
from bot.loader import dp, db
from bot.filters import IsAdmin
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent




@dp.message_handler(IsAdmin(), text="Haydovchilar🚖")
async def show_drivers(message: types.Message):
    await message.answer("Haydovchilar", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Qidirish", switch_inline_query_current_chat="")
            ]
        ]
    ))


@dp.inline_handler(IsAdmin())
async def inline_search(query: types.InlineQuery):
    text = query.query.strip()
    
    if not text:
        drivers = await db.get_drivers_data()
    
    # Search drivers in the database
    results = []
    drivers = await db.search_drivers(text)
    
    for driver in drivers:
        results.append(
            InlineQueryResultArticle(
                id=str(driver['id']),
                title=driver['full_name'],
                description=f"{driver['phone_number']}\n{driver['car_model']} - {driver['car_plate']}\nTarif: {driver['tariff']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"🚖 {driver['car_plate']}"
                ),
            )
        )
    # Send results
    await query.answer(results, cache_time=1)
    
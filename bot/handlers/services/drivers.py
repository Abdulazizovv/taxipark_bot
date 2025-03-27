from aiogram import types
from bot.loader import dp, db
from bot.filters import IsService
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


@dp.inline_handler(IsService(), state="*")
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
                description=f"{driver['phone_number']}\n{driver['car_model']} - {driver['car_plate']}\nBalans: {driver['balance']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"🚖 {driver['car_plate']}"
                ),
            )
        )
    # Send results
    await query.answer(results, cache_time=1)
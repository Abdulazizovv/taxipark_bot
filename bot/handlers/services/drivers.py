from aiogram import types
from bot.loader import dp, db
from bot.filters import IsService
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot.utils.main import format_currency
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import admin_menu_kb


@dp.callback_query_handler(IsService(), text="back_to_admin_panel", state="*")
async def back_to_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Bosh menyudasiz.", reply_markup=admin_menu_kb)
    return


@dp.inline_handler(IsService(), state="*")
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
                title=driver["full_name"] + f" - {driver['phone_number']}",
                description=f"{driver['car_model']} - {driver['car_plate']}\nBalans: {format_currency(int(driver['balance']))}\nTarif: {driver['tariff']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"🚖 {driver['car_plate']}"
                ),
            )
        )

    next_offset = str(offset + limit) if len(drivers) == limit else ""

    await query.answer(results, cache_time=1, next_offset=next_offset)  # Add pagination
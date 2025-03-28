from aiogram import types
from bot.loader import dp, db
from bot.filters import IsAdmin
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot.utils.main import format_currency
from bot.keyboards.default import admin_menu_kb
from aiogram.dispatcher import FSMContext


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
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙 Orqaga",
                        callback_data="back_to_admin_panel"
                    )
                ]
            ]
        ),
    )


@dp.callback_query_handler(IsAdmin(), text="back_to_admin_panel", state="*")
async def back_to_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Bosh menyu.", reply_markup=admin_menu_kb)
    return


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
                title=driver["full_name"] + f" - {driver['phone_number']}",
                description=f"{driver['car_model']} - {driver['car_plate']}\nBalans: {format_currency(int(driver['balance']))}\nTarif: {driver['tariff']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"🚖 {driver['car_plate']}"
                ),
            )
        )

    next_offset = str(offset + limit) if len(drivers) == limit else ""

    await query.answer(results, cache_time=1, next_offset=next_offset)  # Add pagination



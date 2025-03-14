from aiogram import types
from bot.loader import dp, db
from bot.keyboards.inline import driver_cd
from bot.filters import IsAdmin


@dp.callback_query_handler(IsAdmin(), driver_cd.filter())
async def show_driver_info(call: types.CallbackQuery, callback_data: dict):
    driver_id = int(callback_data.get("driver_id"))
    driver = await db.get_driver(driver_id=driver_id)
    await call.message.answer(driver)
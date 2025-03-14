from aiogram import types
from bot.loader import dp, db
from bot.keyboards.inline import admin_menu_cd, admin_menu_kb
from bot.keyboards.inline import drivers_pagination_cd, drivers_pagination_kb
from bot.filters import IsAdmin


@dp.callback_query_handler(admin_menu_cd.filter(action="drivers"), IsAdmin())
async def show_drivers(call: types.CallbackQuery):
    drivers_data = await db.get_drivers_data()
    drivers_text = "".join(
        [
            f"<b>{idx}) {driver['full_name']}</b> - {driver['phone_number']}\n"
            for idx, driver in enumerate(drivers_data, start=1)
        ]
    )
    if not drivers_text:
        drivers_text = "Hozircha haydovchilar ro'yxati bo'sh."
    await call.message.edit_text(
        text="Haydovchilar ro'yxati:\n\n" + drivers_text,
        reply_markup=drivers_pagination_kb(drivers_data, page=1)
    )


@dp.callback_query_handler(drivers_pagination_cd.filter(), IsAdmin())
async def show_drivers_page(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page", 1))
    drivers_data = await db.get_drivers_data(page=page)
    drivers_text = "".join(
        [
            f"<b>{idx}) {driver['full_name']}</b> - {driver['phone_number']}\n"
            for idx, driver in enumerate(drivers_data, start=1)
        ]
    )
    if not drivers_text:
        drivers_text = "Hozircha haydovchilar ro'yxati bo'sh."
    
    await call.message.edit_text(
        text="Haydovchilar ro'yxati:\n\n" + drivers_text,
        reply_markup=drivers_pagination_kb(drivers_data, page)
    )


@dp.callback_query_handler(IsAdmin(), text="main_menu", state="*")
async def back_to_admin_menu(call: types.CallbackQuery):
    await call.message.edit_text("Asosiy menyuga qaytdingiz.", reply_markup=admin_menu_kb)
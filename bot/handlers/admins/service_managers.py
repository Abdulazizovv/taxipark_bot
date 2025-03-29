from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db
from bot.keyboards.inline import service_edit_callback, service_edit_kb
from bot.keyboards.inline.service_managers import select_manager_kb
from bot.filters import IsAdmin


@dp.callback_query_handler(IsAdmin(), service_edit_callback.filter(action="managers"), state="*")
async def show_service_managers(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    service_id = callback_data.get("service_id")
    service = await db.get_service_by_id(service_id)

    if not service.success:
        return await call.message.answer(service.message)

    service = service.data

    managers = await db.get_service_managers(service_id)

    if not managers.success:
        return await call.message.answer(managers.message)

    managers = managers.data

    text = "Menejerlar ro'yxati:\n"\
    "Kerakli menejer tanlang yoki yangi menejer qo'shing."
    await call.message.edit_text(
        text,
        reply_markup=select_manager_kb(managers, service_id),
    )
    await state.finish()
from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import services_kb, admin_menu_kb
from bot.filters import IsAdmin


@dp.message_handler(IsAdmin(), text="Servislar📍", state="*")
async def show_services(message: types.Message, state: FSMContext):
    await state.finish()
    services_response = await db.get_user_services(user_id=message.from_user.id)
    if not services_response.success:
        await message.answer(services_response.message)
        return
    services = services_response.data
    if not services:
        await message.answer("Sizda hali servislar yo'q.", reply_markup=admin_menu_kb)
        return

    await message.answer("Barcha servislar:", reply_markup=services_kb(services))

    await state.set_state("select_service")
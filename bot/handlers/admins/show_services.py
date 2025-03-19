from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import services_kb


@dp.message_handler(text="Servislar📍", state="*")
async def show_services(message: types.Message, state: FSMContext):
    await state.finish()
    services_response = await db.get_all_services()
    if not services_response.success:
        await message.answer("Servislar ro'yxati bo'sh")
        return
    services = services_response.data

    await message.answer("Barcha servislar:", reply_markup=services_kb(services))

    await state.set_state("select_service")
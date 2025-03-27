from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default.service import select_service_keyboard


@dp.message_handler(IsService(), text="📝 Xizmatlar", state="*")
async def start_service(message: types.Message, state: FSMContext):
    await state.finish()
    services = await db.get_user_services(message.from_user.id)
    if not services.success:
        return await message.answer(services.message)
    services = services.data
    
    await message.answer("Xizmat ko'rsatish uchun tanlang", reply_markup=select_service_keyboard(services))
    await state.set_state("select_service")
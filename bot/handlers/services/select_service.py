from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default.service import select_service_category_keyboard


@dp.message_handler(IsService(), state="select_service")
async def select_service(message: types.Message, state: FSMContext):
    service = await db.get_service_by_title(message.text)
    if not service.success:
        return await message.answer(service.message)
    service = service.data
    await state.update_data(service_id=service['id'])

    await message.answer(f"Siz {service['title']} xizmatini tanladingiz.\n"
                         f"Xizmat kategoriyasini tanlang:", reply_markup=select_service_category_keyboard(service['categories']))
    
    await state.set_state("select_service_category")
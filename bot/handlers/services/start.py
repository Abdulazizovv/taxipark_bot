from bot.filters import IsService
from bot.loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import service_admin_menu_kb


@dp.message_handler(IsService(), commands=['start'], state="*")
async def service_start(message: types.Message, state: FSMContext):

    await state.finish()

    await message.answer("Assalomu alaykum! \n\n", reply_markup=service_admin_menu_kb)
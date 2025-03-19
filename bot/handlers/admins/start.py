from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
from aiogram.dispatcher.filters import Command
from bot.keyboards.default import admin_menu_kb
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command("start"), IsAdmin(), state="*")
async def admin_bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Assalomu alaykum, admin!", reply_markup=admin_menu_kb)

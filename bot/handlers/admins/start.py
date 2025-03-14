from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
from aiogram.dispatcher.filters import CommandStart
from bot.keyboards.inline import admin_menu_kb


@dp.message_handler(CommandStart, IsAdmin())
async def admin_bot_start(message: types.Message):
    await message.answer("Assalomu alaykum, admin!", reply_markup=admin_menu_kb)
    
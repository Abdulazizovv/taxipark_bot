from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
from aiogram.dispatcher.filters import CommandStart


@dp.message_handler(CommandStart, IsAdmin())
async def admin_bot_start(message: types.Message):
    await message.answer("You are admin! You can use all commands!")
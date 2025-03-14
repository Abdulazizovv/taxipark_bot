from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.loader import db


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return await db.bot_user_role(message.from_user.id) == 'admin'

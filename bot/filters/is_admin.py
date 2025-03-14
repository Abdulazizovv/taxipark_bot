from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.loader import db


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return await db.user_is_admin(message.from_user.id)

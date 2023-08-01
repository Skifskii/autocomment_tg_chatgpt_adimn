from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api.quick_commands import user as db_users


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        try:
            user = await db_users.select_user(message.from_user.id)
            return user.status == 'admin'
        except AttributeError:
            return False

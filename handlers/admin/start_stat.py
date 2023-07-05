import datetime

from aiogram import types

from loader import dp
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import stat as db_stat

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='start_stat')
async def start_stat(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        if len(await db_stat.take_stat()) < 1:
            await db_stat.add_row_to_stats(str(datetime.datetime.today()))
            await log_all('start_stat', 'info', message.from_user.id, message.from_user.first_name, 'Row added')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('start_stat', 'error', message.from_user.id, message.from_user.first_name, error)

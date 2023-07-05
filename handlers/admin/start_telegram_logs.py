from aiogram import types

from loader import dp
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import telegram_log_permission as db_tgperms

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='start_tg_logs')
async def start_tg_logs(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        if len(await db_tgperms.select_permissions()) < 1:
            await db_tgperms.add_row_to_tg_log_permissions()
            await log_all('start_tg_logs', 'info', message.from_user.id, message.from_user.first_name, 'Row added')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('start_stat', 'error', message.from_user.id, message.from_user.first_name, error)

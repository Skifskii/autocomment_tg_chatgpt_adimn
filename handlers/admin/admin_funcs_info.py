from aiogram import types

from loader import dp
from utils.db_api.quick_commands import user as db_users

from data.texts import unknown_error_answer, admin_funcs_info_answer
from logs.log_all import log_all


@dp.message_handler(commands='admin')
async def admin_funcs_info(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        await message.answer(admin_funcs_info_answer)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('admin_funcs_info', 'error', message.from_user.id, message.from_user.first_name, error)

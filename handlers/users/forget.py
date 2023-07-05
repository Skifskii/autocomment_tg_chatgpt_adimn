from aiogram import types

from loader import dp
from utils.db_api.quick_commands import user as db_users

from data.texts import forget_answer, unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='forget')
async def command_forget(message: types.Message):
    try:
        await db_users.clear_story(message.from_user.id)
        await message.answer(forget_answer)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('forget', 'error', message.from_user.id, message.from_user.first_name, error)

from aiogram import types

from loader import dp

from data.texts import about_answer, unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='about')
async def command_about(message: types.Message):
    try:
        await message.answer(about_answer)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('about', 'error', message.from_user.id, message.from_user.first_name, error)

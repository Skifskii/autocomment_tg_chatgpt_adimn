from aiogram import types

from loader import dp

from data.texts import help_answer, unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='help')
async def command_help(message: types.Message):
    try:
        await message.answer(help_answer)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('help', 'error', message.from_user.id, message.from_user.first_name, error)

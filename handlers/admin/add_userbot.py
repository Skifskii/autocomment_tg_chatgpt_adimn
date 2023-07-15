from aiogram import types

from loader import dp
from utils.db_api.quick_commands import userbot as db_userbot
from utils.db_api.quick_commands import telegram_log_permission as db_tgperms

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='add_userbot')
async def add_userbot(message: types.Message):
    try:
        await db_userbot.add_userbot(1)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('start_stat', 'error', message.from_user.id, message.from_user.first_name, error)

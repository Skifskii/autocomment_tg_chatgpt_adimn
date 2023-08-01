from aiogram import types

from loader import dp
from utils.db_api.quick_commands import userbot as db_userbots

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='i_am_new_userbot')
async def command_i_am_new_userbot(message: types.Message):
    try:
        userbot = await db_userbots.select_userbot(message.from_user.id)
        if not userbot:
            await db_userbots.add_userbot(telegram_id=message.from_user.id)
            await db_userbots.reset_firstname(message.from_user.id, message.from_user.first_name)
            await db_userbots.reset_lastname(message.from_user.id, message.from_user.last_name)
            await db_userbots.reset_phone(message.from_user.id, message.get_args().split('_')[0])
            await db_userbots.reset_proxy(message.from_user.id, message.get_args().split('_')[1])
            await log_all('i_am_new_userbot', 'info', message.from_user.id, message.from_user.first_name, 'New userbot')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('i_am_new_userbot', 'error', message.from_user.id, message.from_user.first_name, error)

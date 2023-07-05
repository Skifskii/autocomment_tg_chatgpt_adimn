from aiogram import types

from loader import dp, bot
from utils.db_api.quick_commands import user as db_users

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='send_to_users')
async def send_to_users(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        message_to_sent = message.get_args()
        users = await db_users.select_all_users()
        for user in users:
            try:
                await bot.send_message(user.user_id, message_to_sent)
            except Exception as error:
                await log_all('send_to_users', 'error', user.user_id, user.firstname, error)
        await log_all('send_to_users', 'info', message.from_user.id, message.from_user.first_name, f'Message to users:\n{message_to_sent}')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('send_to_users', 'error', message.from_user.id, message.from_user.first_name, error)

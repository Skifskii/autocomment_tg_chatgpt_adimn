from datetime import date, timedelta

from aiogram import types

from loader import dp, bot
from utils.db_api.quick_commands import user as db_users

from data.texts import start_answer, unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(commands='start_userbots')
async def command_start(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)

        userbot = user.userbots.split(' @@ ; @@ ')[1:]
        ub_id, ub_username, ub_firstname, ub_lastname = userbot[0].split(' @@ , @@ ')

        groups = user.groups.split(' @@ ; @@ ')[1:]
        for group in groups:
            try:
                group_name, group_link = group.split(' @@ , @@ ')
                await bot.send_message(ub_id, group_link)
            except Exception as error:
                await message.answer(unknown_error_answer)
                await log_all('start', 'error', message.from_user.id, message.from_user.first_name, error)
                return
        await message.answer('Юзерботы готовы к работе!')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('start', 'error', message.from_user.id, message.from_user.first_name, error)

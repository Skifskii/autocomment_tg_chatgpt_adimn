from aiogram import types

from loader import dp, bot
from utils.db_api.quick_commands import user as db_users, userbot as db_userbots

from data.texts import unknown_error_answer, userbots_list_is_empty_message
from logs.log_all import log_all


@dp.message_handler(commands='start_userbots')
async def command_start_userbots(message: types.Message):
    try:
        userbots = await db_users.get_userbots(message.from_user.id)
        channels = await db_users.get_channels(message.from_user.id)

        if not userbots:
            await message.answer(userbots_list_is_empty_message)
            return

        for userbot_id in userbots:
            try:
                userbot = await db_userbots.select_userbot(int(userbot_id))
                await bot.send_message(userbot.telegram_id, f'join_channels {message.from_user.id}')
                await message.answer('Начинаю подписку на каналы...')
            except Exception as error:
                await message.answer(unknown_error_answer)
                await log_all('start_userbots_function', 'error', message.from_user.id, message.from_user.first_name, error)
                return
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('start_userbots', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler()
async def catch_userbot_messages(message: types.Message):
    try:
        userbot = await db_userbots.select_userbot(message.from_user.id)
        if userbot is None:
            return

        if ' : channel does not exist' in message.text:
            await bot.send_message(userbot.owner_id, f'❌ <b>Ошибка</b> при подключении к каналу {message.text.split(" ")[0]}.\nКанал не найден.')
        if ' : joined channel successfully' in message.text:
            await bot.send_message(userbot.owner_id, f'✅ Юзербот <b>успешно</b> подписался на канал {message.text.split(" ")[0]}')
        if ' : unknown error' in message.text:
            await bot.send_message(userbot.owner_id, f'❌ <b>Ошибка</b> при подключении к каналу {message.text.split(" ")[0]}')
    except Exception as error:
        await log_all('catch_userbot_messages', 'error', message.from_user.id, message.from_user.first_name, error)

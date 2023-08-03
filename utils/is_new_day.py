import asyncio
from datetime import date

from loader import bot
from logs.log_all import log_all
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import userbot as db_userbots


async def set_new_day():
    userbots = await db_userbots.select_all_userbots()
    for userbot in userbots:
        await bot.send_message(userbot.telegram_id, f'are_you_here')
        await asyncio.sleep(2)
    await asyncio.sleep(5)

    userbots = await db_userbots.select_all_userbots()
    dead_userbots = []
    for userbot in userbots:
        if userbot.alive == 0:
            dead_userbots.append(userbot.phone)

    dead_userbots_str = ''
    if len(dead_userbots) > 0:
        dead_userbots_str = ''
        for dead_userbot in dead_userbots:
            dead_userbots_str += dead_userbot
            dead_userbots_str += '\n'
        users = await db_users.select_all_users()
        for user in users:
            if user.status == 'admin':
                await bot.send_message(user.user_id, f'Сегодня умерло <b>{len(dead_userbots)}</b> юзерботов:\n\n{dead_userbots_str}')
    for userbot in userbots:
        await db_userbots.reset_alive(userbot.telegram_id, 0)

import asyncio
from datetime import date

from loader import bot
from logs.log_all import log_all
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import userbot as db_userbots
from utils.db_api.quick_commands import stat as db_stat


async def set_new_day():
    userbots = await db_userbots.select_all_userbots()
    for userbot in userbots:
        await bot.send_message(userbot.telegram_id, f'are_you_here')
        await asyncio.sleep(2)
    await asyncio.sleep(5)
    stat = await db_stat.take_stat()
    num_of_alive_userbots = stat.num_of_alive_userbots
    if len(userbots) > num_of_alive_userbots:
        users = await db_users.select_all_users()
        for user in users:
            if user.status == 'admin':
                await bot.send_message(user.user_id, '')

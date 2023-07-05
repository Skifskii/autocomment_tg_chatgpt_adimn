from aiogram import Dispatcher, types
from logs.logging_loguru.logger import logger
from utils.db_api.quick_commands import user as db_users


async def notify_admins(dp: Dispatcher, text: str):
    try:
        users = await db_users.select_all_users()
        for user in users:
            if user.status == 'admin':
                await dp.bot.send_message(chat_id=user.user_id, text=text, parse_mode=types.ParseMode.MARKDOWN)
    except Exception as error:
        logger.error(f'in notify_admins :: {error}')

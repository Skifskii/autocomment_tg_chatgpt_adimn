from asyncpg import UniqueViolationError

from utils.db_api.schemas.telegram_log_permission import TelegramLogPermission
from logs.logging_loguru.logger import logger

async def add_row_to_tg_log_permissions():
    try:
        perms = TelegramLogPermission()
        await perms.create()
    except UniqueViolationError as error:
        logger.error(f"in add_row_to_tg_log_permissions :: {error}")


async def select_permissions():
    perms = (await TelegramLogPermission.query.gino.all())
    return perms


async def reset_permissions(new_statuses):
    perms = (await TelegramLogPermission.query.gino.all())[0]
    await perms.update(info=new_statuses[0], warning=new_statuses[1], error=new_statuses[2]).apply()

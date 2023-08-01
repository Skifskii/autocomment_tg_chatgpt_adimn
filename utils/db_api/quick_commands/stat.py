from asyncpg import UniqueViolationError

from logs.log_all import log_all
from utils.db_api.schemas.stat import EverydayStats


async def take_stat():
    stat = await EverydayStats.query.gino.all()
    return stat[0]

from asyncpg import UniqueViolationError

from logs.log_all import log_all
from utils.db_api.schemas.stat import EverydayStats


async def add_row_to_stats(date_start):
    try:
        stat = EverydayStats(date_start=date_start)
        await stat.create()
    except UniqueViolationError as error:
        await log_all('add_row_to_stats', 'error', '', '', f'Row did not added: {error}')


async def add_new_user_to_stats():
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(num_of_new_users=stat.num_of_new_users + 1).apply()


async def add_new_request_to_stats():
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(num_of_new_requests=stat.num_of_new_requests + 1).apply()


async def add_new_answer_to_stats():
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(num_of_new_answers=stat.num_of_new_answers + 1).apply()


async def add_new_tokens_to_stats(tokens):
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(num_of_tokens=stat.num_of_tokens + tokens).apply()


async def add_new_date(date):
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(date_start=date).apply()


async def take_stat():
    stat = await EverydayStats.query.gino.all()
    return stat


async def reset_stat(date):
    stat = (await EverydayStats.query.gino.all())[0]
    await stat.update(date_start=date, num_of_new_users=0, num_of_new_requests=0, num_of_new_answers=0, num_of_tokens=0).apply()

from asyncpg import UniqueViolationError

from logs.log_all import log_all
from utils.db_api.schemas.openai_api_key import OpeanaiApiKey


async def add_key(new_key):
    try:
        key = OpeanaiApiKey(key=new_key)
        await key.create()
    except UniqueViolationError as error:
        await log_all('add_key', 'error', '', '', f'Row did not added: {error}')


async def select_all_keys():
    keys = await OpeanaiApiKey.query.gino.all()
    return keys


async def delete_key(key):
    await OpeanaiApiKey.delete.where(OpeanaiApiKey.key == key).gino.status()

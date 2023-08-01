from asyncpg import UniqueViolationError

from logs.log_all import log_all
from utils.db_api.schemas.proxy import Proxy


async def add_proxy(new_proxy):
    try:
        proxy = Proxy(proxy_data=new_proxy)
        await proxy.create()
    except UniqueViolationError as error:
        await log_all('add_proxy', 'error', '', '', f'Row did not added: {error}')


async def select_proxy(proxy_data):
    proxy = await Proxy.query.where(Proxy.proxy_data == proxy_data).gino.first()
    return proxy


async def select_all_proxies():
    proxies = await Proxy.query.gino.all()
    return proxies


async def reset_accounts_number(proxy_data):
    proxy = await select_proxy(proxy_data)
    await proxy.update(accounts_number=proxy.accounts_number + 1).apply()

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from loader import dp
from utils.db_api.quick_commands import proxy as db_proxies
from states.new_proxy import NewProxy

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(IsAdmin(), commands='manage_proxy')
async def manage_openai_api_key(message: types.Message):
    try:
        proxies = await db_proxies.select_all_proxies()
        await message.answer(f'На данный момент используется <b>{len(proxies)}</b> proxy\n\n/check_proxy - посмотреть\n/add_proxy - добавить')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('manage_openai_api_key', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(IsAdmin(), commands='add_proxy')
async def add_proxy(message: types.Message):
    try:
        await message.answer('Введите данные прокси. Если вы хотите подключить несколько прокси, введите их столбиком.')
        await NewProxy.new_proxy.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('add_proxy', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(state=NewProxy.new_proxy)
async def get_proxy(message: types.Message, state: FSMContext):
    try:
        new_proxies = message.text.split('\n')
        for proxy_data in new_proxies:
            await db_proxies.add_proxy(proxy_data)
        await message.answer('Прокси добавлены!')
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('get_proxy', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(IsAdmin(), commands='check_proxy')
async def check_proxy(message: types.Message):
    try:
        proxies = await db_proxies.select_all_proxies()
        proxies_list_message = 'Список proxy:\n\n'
        for proxy in proxies:
            proxies_list_message += proxy.proxy_data
            proxies_list_message += '\n'

        await message.answer(proxies_list_message)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('check_proxy', 'error', message.from_user.id, message.from_user.first_name, error)

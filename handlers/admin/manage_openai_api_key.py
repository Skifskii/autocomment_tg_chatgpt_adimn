from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from loader import dp
from utils.db_api.quick_commands import openai_api_key as db_openai_api_keys
from states.new_openai_api_key import NewOpenaiApiKey

from data.texts import unknown_error_answer
from logs.log_all import log_all


@dp.message_handler(IsAdmin(), commands='manage_openai_api_key')
async def manage_openai_api_key(message: types.Message):
    try:
        keys = await db_openai_api_keys.select_all_keys()
        await message.answer(f'На данный момент используется <b>{len(keys)}</b> ключей\n\n/check_openai_api_keys - посмотреть\n/add_openai_api_keys - добавить')
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('manage_openai_api_key', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(IsAdmin(), commands='add_openai_api_keys')
async def add_openai_api_key(message: types.Message):
    try:
        await message.answer('Введите ключи OpenAI API. Если вы хотите подключить несколько ключей, введите их столбиком.')
        await NewOpenaiApiKey.new_openai_api_key.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('add_openai_api_key', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(IsAdmin(), state=NewOpenaiApiKey.new_openai_api_key)
async def get_openai_api_key(message: types.Message, state: FSMContext):
    try:
        new_keys = message.text.split('\n')

        for key in new_keys:
            await db_openai_api_keys.add_key(key)

        await message.answer('Ключи добавлены!')
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('get_openai_api_key', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(IsAdmin(), commands='check_openai_api_keys')
async def check_openai_api_keys(message: types.Message):
    try:
        keys = await db_openai_api_keys.select_all_keys()
        key_list_message = 'Список ключей:\n\n'
        for key in keys:
            key_list_message += key.key
            key_list_message += '\n'

        await message.answer(key_list_message)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('check_openai_api_keys', 'error', message.from_user.id, message.from_user.first_name, error)

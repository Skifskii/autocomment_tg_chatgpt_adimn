import json
from datetime import date

import openai
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ChatActions
from deep_translator import GoogleTranslator

from data.texts import while_answer_is_generating_answer, ask_gpt_without_subscribe_answer, ban_answer, \
    ask_dalle_without_subscribe_answer, image_command_answer, choose_image_size_message, unknown_error_answer, \
    generating_image_message, openai_dalle_error_message, openai_dalle_bad_request_error_message, \
    subscription_finished_message
from keyboards.inline import ikb_image_size
from loader import dp, bot
from states import Image
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import stat as db_stat

from logs.log_all import log_all
from utils.openai_api.dalle import request_to_dalle
from utils.openai_api.gpt import request_to_gpt


@dp.message_handler(Command('image'), state=None)
async def image_command(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status == 'user' or user.status == 'gpt':
            await message.answer(ask_dalle_without_subscribe_answer)
            return
        if user.status == 'ban':
            await message.answer(ban_answer)
            return
        if user.status != 'admin' and user.date_subscription_finish <= str(date.today()):
            await message.answer(subscription_finished_message)
            return
        await message.answer(image_command_answer)
        await Image.prompt.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('image_command', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(state=Image.prompt)
async def choose_image_size(message: types.Message, state: FSMContext):
    try:
        new_prompt = message.text
        translated_prompt = GoogleTranslator(source='auto', target='english').translate(text=new_prompt)
        await state.update_data(prompt=new_prompt, translated_prompt=translated_prompt)
        await message.answer(choose_image_size_message, reply_markup=ikb_image_size)
        await Image.size.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('prompt', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_size', state=Image.size)
async def generate_image(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_prompt = data.get('prompt')
    translated_prompt = data.get('translated_prompt')
    try:
        new_size = query.data.split('_')[-1]
        new_size = f'{new_size}x{new_size}'

        await query.message.edit_text(generating_image_message)

        photo = await request_to_dalle(translated_prompt, new_size)

        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await bot.send_chat_action(query.message.chat.id, ChatActions.UPLOAD_PHOTO)
        await bot.send_photo(query.message.chat.id, photo)

        await db_users.commit_new_image(user_id=query.from_user.id)

        await log_all('generate_image',
                      'info',
                      query.from_user.id,
                      query.from_user.first_name,
                      f'Prompt: {new_prompt}\nTranslated prompt: {translated_prompt}\nAnswer: {photo}')
    except openai.error.APIError as error:
        await log_all('generate_image', 'warning', query.from_user.id, query.from_user.first_name, error)
        await bot.send_message(query.message.chat.id, openai_dalle_error_message)
    except openai.error.InvalidRequestError as error:
        await log_all('generate_image', 'warning', query.from_user.id, query.from_user.first_name, f'{error}\nprompt: {new_prompt}\ntranslated prompt: {translated_prompt}')
        await bot.send_message(query.message.chat.id, openai_dalle_bad_request_error_message)
    except Exception as error:
        await log_all('generate_image', 'error', query.from_user.id, query.from_user.first_name, error)
        await bot.send_message(query.message.chat.id, unknown_error_answer)
    await state.finish()

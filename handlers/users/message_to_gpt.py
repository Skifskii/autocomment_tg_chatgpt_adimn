from datetime import date

import json

import aiogram
import openai
from aiogram import types
from aiogram.types import ChatActions

from data.texts import while_answer_is_generating_answer, ask_gpt_without_subscribe_answer, ban_answer, \
    unknown_error_answer, subscription_finished_message, RateLimitError_answer, InvalidRequestError_answer
from loader import dp, bot
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import stat as db_stat

from logs.log_all import log_all
from utils.openai_api.gpt import request_to_gpt


@dp.message_handler()
async def send(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        await db_users.set_username(user.user_id, message.from_user.username)
        if user.status == 'user':
            await message.answer(ask_gpt_without_subscribe_answer)
            return
        if user.status == 'ban':
            await message.answer(ban_answer)
            return
        if user.status != 'admin' and user.date_subscription_finish <= str(date.today()):
            await message.answer(subscription_finished_message)
            return
        answer_generating_message = await message.answer(while_answer_is_generating_answer)
        await db_stat.add_new_request_to_stats()
        messages = json.loads(await db_users.get_story(message.from_user.id))
        messages['messages'].append({"role": "user", "content": message.text})

        gpt_answer, tokens_spent = await request_to_gpt(messages['messages'])
        # gpt_answer, tokens_spent = 'hi', 1

        await bot.delete_message(answer_generating_message.chat.id, answer_generating_message.message_id)
        try:
            await message.answer(gpt_answer, parse_mode=types.ParseMode.MARKDOWN)
        except aiogram.utils.exceptions.CantParseEntities as error:
            await message.answer(gpt_answer, parse_mode=types.ParseMode.HTML)
        messages['messages'].append({"role": "assistant", "content": gpt_answer})

        def replace_bsn_from_start(s):
            while s.startswith('\n'):
                s = s[1:]
            return s

        await db_users.add_story(user_id=message.from_user.id, messages=json.dumps(messages))
        await db_stat.add_new_answer_to_stats()
        await db_stat.add_new_tokens_to_stats(tokens_spent)
        await db_users.commit_new_message(user_id=message.from_user.id)
        await log_all('message_to_gpt', 'info', message.from_user.id, message.from_user.first_name, f'\n--------------------\nMessage:\n{message.text}\n\nAnswer:\n{replace_bsn_from_start(gpt_answer)}\n--------------------')
    except openai.error.InvalidRequestError as error:
        await db_users.clear_story(message.from_user.id)
        await message.answer(InvalidRequestError_answer)
        await log_all('message_to_gpt', 'error', message.from_user.id, message.from_user.first_name,
                      f'openai.error.InvalidRequestError - {error}')
    except openai.error.RateLimitError as error:
        await message.answer(RateLimitError_answer)
        await log_all('message_to_gpt', 'error', message.from_user.id, message.from_user.first_name, f'openai.error.RateLimitError - {error}')
    except Exception as error:
        await message.answer(unknown_error_answer)
        print(Exception.with_traceback())
        await log_all('message_to_gpt', 'error', message.from_user.id, message.from_user.first_name, error)

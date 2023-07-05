import datetime

from aiogram import types

from loader import dp
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import stat as db_stat

from data.texts import unknown_error_answer, stat_answer
from logs.log_all import log_all


@dp.message_handler(commands='stat')
async def stat(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        statistic = (await db_stat.take_stat())[0]
        today = f"""{datetime.date.today()}  {datetime.time(datetime.datetime.now().time().hour, datetime.datetime.now().time().minute).isoformat(timespec='minutes')}"""
        total_number_of_messages = 0
        total_number_of_images = 0
        users = await db_users.select_all_users()
        for user in users:
            total_number_of_messages += user.total_messages_sent
            total_number_of_images += user.total_images_generated
        await message.answer(stat_answer.format(date_start=statistic.date_start,
                                                today=today,
                                                num_of_new_users=statistic.num_of_new_users,
                                                num_of_new_requests=statistic.num_of_new_requests,
                                                num_of_new_answers=statistic.num_of_new_answers,
                                                num_of_tokens=statistic.num_of_tokens,
                                                total_num_of_users=len(await db_users.select_all_users()),
                                                total_number_of_messages=total_number_of_messages,
                                                total_number_of_images=total_number_of_images))
        await db_stat.reset_stat(today)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('stat', 'error', message.from_user.id, message.from_user.first_name, error)

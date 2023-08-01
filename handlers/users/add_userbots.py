from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.db_api.quick_commands import user as db_users, userbot as db_userbots

from data.texts import unknown_error_answer, userbots_list_is_empty_message
from logs.log_all import log_all
from states.number_of_new_userbots import NumberOfNewUserbots


@dp.message_handler(commands='add_userbots')
async def command_add_userbots(message: types.Message):
    try:
        userbots = await db_userbots.select_all_userbots()
        counter = 0
        for userbot in userbots:
            if userbot.owner_id == -1:
                counter += 1

        def ten_or_lower(c):
            if c < 10:
                return c
            return 10

        await message.answer(f'На данный момент у нас есть {counter} свободных юзерботов.\nСколько юзерботов вы хотите приобрести? Введите число <b>от 1 до {ten_or_lower(counter)}</b>')
        await NumberOfNewUserbots.number_of_new_userbots.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('add_userbots', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.message_handler(state=NumberOfNewUserbots.number_of_new_userbots)
async def add_userbots(message: types.Message, state: FSMContext):
    try:
        number_of_new_userbots = message.text
        try_number_of_new_userbots = int(number_of_new_userbots)

        userbots = await db_userbots.select_all_userbots()

        counter = 0
        for userbot in userbots:
            if userbot.owner_id == -1:
                counter += 1

        if not 1 <= try_number_of_new_userbots <= counter:
            await bot.send_message(message.from_user.id,
                                   f'Число должно находиться в интервале от 1 до {counter}. Чтобы повторить попытку, нажмите /add_userbot')
            await state.finish()
            return

        counter = 0
        for userbot in userbots:
            if userbot.owner_id == -1:
                counter += 1
                await db_userbots.reset_owner_id(userbot.telegram_id, message.from_user.id)
                await db_users.add_userbot(message.from_user.id, str(userbot.telegram_id))
            if counter == try_number_of_new_userbots:
                break

        await message.answer(f'Вам доступно <b>{number_of_new_userbots}</b> новых юзерботов!\nНастройте их, нажав /my_userbots')
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('add_userbots', 'error', message.from_user.id, message.from_user.first_name, error)

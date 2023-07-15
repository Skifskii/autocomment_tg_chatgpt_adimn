from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import ikb_subscribe, ikb_manage_channels, ikb_manage_userbots, ikb_edit_userbot, ikb_reset_sex, \
    ikb_sure_reset_age, ikb_reset_use_emoji, ikb_reset_commenting_posts, ikb_reset_chat_in_comments, \
    ikb_reset_chat_in_groups, ikb_sure_reset_gpt_task, ikb_reset_common_settings, ikb_manage_common_settings, \
    ikb_add_keywords, ikb_sure_reset_firstname, ikb_sure_reset_lastname, ikb_sure_reset_bio
from loader import dp, bot
from states import NewAge, NewGptTask, TakeNewSubscribeData, TakeNewAnswerData, TakeNewKeywords, NewFirstname, \
    NewLastname, NewBio
from utils.db_api.quick_commands import user as db_users, userbot as db_userbots
from utils.yookassa_api.new_payment import create_new_payment, check_payment_status

from data.config import subscriptions_dict, subscription_prices
from data.texts import profile_answer, buy_no_email_answer, select_subscription_message, \
    choose_subscription_type_answer, \
    unknown_error_answer, payment_link_message, invalid_email_value_type, userbots_list_message, \
    userbots_list_is_empty_message
from logs.log_all import log_all


async def create_userbot_profile(user_id, page_number: int = 1) -> str:
    userbots = await db_users.get_userbots(user_id)
    this_userbot = await db_userbots.select_userbot(int(userbots[page_number - 1]))

    def bool_translator(b):
        if b:
            return 'Да'
        return 'Нет'

    def sex_translator(s):
        if s == 'm':
            return 'М'
        else:
            return 'Ж'

    answer = userbots_list_message.format(
        firstname = this_userbot.firstname,
        lastname = this_userbot.lastname,
        bio = this_userbot.bio,
        sex = sex_translator(this_userbot.sex),
        age = this_userbot.age,
        gpt_task = this_userbot.gpt_task,
        use_emoji = bool_translator(this_userbot.use_emoji),
        commenting_posts = bool_translator(this_userbot.commenting_posts),
        chat_in_comments = bool_translator(this_userbot.chat_in_comments),
        chat_in_groups = bool_translator(this_userbot.chat_in_groups),
        page_number = page_number,
        total_number_of_pages = len(userbots)
    )
    return answer


@dp.message_handler(commands='my_userbots')
async def command_my_userbots(message: types.Message):
    try:
        userbots = await db_users.get_userbots(message.from_user.id)

        if not userbots:
            await message.answer(userbots_list_is_empty_message)
            return

        answer = await create_userbot_profile(message.from_user.id)
        await message.answer(answer, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('command_my_userbots', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_move_')
async def btn_move_pressed(query: types.CallbackQuery):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        new_page_number = -1

        if query.data.split('_')[-1] == 'right':
            if this_page_number < max_page_number:
                new_page_number = this_page_number + 1
        else:
            if this_page_number > 1:
                new_page_number = this_page_number - 1

        if new_page_number == -1:
            return

        new_page = await create_userbot_profile(query.from_user.id, page_number=new_page_number)
        await query.message.edit_text(new_page, reply_markup=ikb_manage_channels)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_move_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_common_settings')
async def btn_common_settings_pressed(query: types.CallbackQuery):
    try:
        user = await db_users.select_user(query.from_user.id)
        await query.message.edit_text("""
<b>Общие настройки:</b>
        
- Время задержки подписок: <i>{subscribe_delay} сек.</i>
- Время задержки ответа: <i>{answer_delay} сек.</i>
- Ключевые слова: <code>{keywords}</code>""".format(subscribe_delay=user.subscribe_delay,
                                                    answer_delay=user.answer_delay,
                                                    keywords=user.keywords),
                                      reply_markup=ikb_reset_common_settings)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_common_settings_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_reset_common_settings')
async def btn_edit_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_manage_common_settings)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_edit', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_reset_delay_subscribe')
async def btn_reset_delay_subscribe_pressed(query: types.CallbackQuery):
    try:
        user = await db_users.select_user(query.from_user.id)
        await query.message.edit_text(f'Текущее время задержки подписки - {user.subscribe_delay} сек.\n\nВведите одно число: новое время задержки (сек.)')
        await TakeNewSubscribeData.new_data.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_delay_subscribe_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=TakeNewSubscribeData.new_data)
async def take_new_delay_subscribe(message: types.Message, state: FSMContext):
    try:
        new_delay = message.text
        new_delay = int(new_delay)

        if new_delay < 1:
            await bot.send_message(message.from_user.id,
                                   'Число должно быть больше, чем 0')
            return
        await db_users.set_subscribe_delay(message.from_user.id, new_delay)
        await state.finish()

        user = await db_users.select_user(message.from_user.id)
        await message.answer("""
<b>Общие настройки:</b>

- Время задержки подписок: <i>{subscribe_delay} сек.</i>
- Время задержки ответа: <i>{answer_delay} сек.</i>
- Ключевые слова: <code>{keywords}</code>""".format(subscribe_delay=user.subscribe_delay,
                                                    answer_delay=user.answer_delay,
                                                    keywords=user.keywords),
                             reply_markup=ikb_reset_common_settings)

    except ValueError as error:
        await message.answer('Введите одно число\nНапример: 100')
        await log_all('take_new_delay_subscribe', 'warning', message.from_user.id, message.from_user.first_name, error)
    except Exception as error:
        await state.finish()
        await message.answer(unknown_error_answer)
        await log_all('take_new_delay_subscribe', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_reset_delay_answer')
async def btn_reset_delay_answer_pressed(query: types.CallbackQuery):
    try:
        user = await db_users.select_user(query.from_user.id)
        await query.message.edit_text(f'Текущее время задержки ответов - {user.answer_delay} сек.\n\nВведите одно число: новое время задержки (сек.)')
        await TakeNewAnswerData.new_data.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_delay_answer_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=TakeNewAnswerData.new_data)
async def take_new_delay_answer(message: types.Message, state: FSMContext):
    try:
        new_delay = message.text
        new_delay = int(new_delay)

        if new_delay < 1:
            await bot.send_message(message.from_user.id,
                                   'Число должно быть больше, чем 0')
            return
        await db_users.set_answer_delay(message.from_user.id, new_delay)
        await state.finish()

        user = await db_users.select_user(message.from_user.id)
        await message.answer("""
<b>Общие настройки:</b>

- Время задержки подписок: <i>{subscribe_delay} сек.</i>
- Время задержки ответа: <i>{answer_delay} сек.</i>
- Ключевые слова: <code>{keywords}</code>""".format(subscribe_delay=user.subscribe_delay,
                                                    answer_delay=user.answer_delay,
                                                    keywords=user.keywords),
                             reply_markup=ikb_reset_common_settings)

    except ValueError as error:
        await message.answer('Введите одно число\nНапример: 100')
        await log_all('take_new_delay_answer', 'warning', message.from_user.id, message.from_user.first_name, error)
    except Exception as error:
        await state.finish()
        await message.answer(unknown_error_answer)
        await log_all('take_new_delay_answer', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_reset_keywords')
async def btn_reset_keywords_pressed(query: types.CallbackQuery):
    try:
        user = await db_users.select_user(query.from_user.id)
        if user.keywords == '':
            await query.message.edit_text(f'Сейчас у вас нет ключевых слов. Хотите добавить?', reply_markup=ikb_add_keywords)
        else:
            await query.message.edit_text(f'Список ваших ключевых слов:\n<code>{user.keywords}</code>\n\nХотите изменить список?', reply_markup=ikb_add_keywords)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_keywords_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_keywords_cancel')
async def btn_cancel_keywords_pressed(query: types.CallbackQuery):
    try:
        await bot.delete_message(query.from_user.id, query.message.message_id)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_cancel_keywords_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_keywords_add')
async def btn_add_keywords_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Введите ключевые слова через запятую.\nНапример: "привет, новости, ты"')
        await TakeNewKeywords.new_data.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_add_keywords_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=TakeNewKeywords.new_data)
async def take_new_delay_answer(message: types.Message, state: FSMContext):
    try:
        new_data = message.text
        new_keywords = new_data.split(', ')

        await db_users.set_new_keywords(message.from_user.id, new_data)
        await state.finish()

        user = await db_users.select_user(message.from_user.id)
        await message.answer("""
<b>Общие настройки:</b>

- Время задержки подписок: <i>{subscribe_delay} сек.</i>
- Время задержки ответа: <i>{answer_delay} сек.</i>
- Ключевые слова: <code>{keywords}</code>""".format(subscribe_delay=user.subscribe_delay,
                                                    answer_delay=user.answer_delay,
                                                    keywords=user.keywords),
                             reply_markup=ikb_reset_common_settings)

    except ValueError as error:
        await message.answer('Введите одно число\nНапример: 100')
        await log_all('take_new_delay_answer', 'warning', message.from_user.id, message.from_user.first_name, error)
    except Exception as error:
        await state.finish()
        await message.answer(unknown_error_answer)
        await log_all('take_new_delay_answer', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_edit')
async def btn_edit_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_edit_userbot)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_edit', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# firstname
@dp.callback_query_handler(text_contains='btn_reset_firstname')
async def btn_reset_firstname_pressed(query: types.CallbackQuery):
    try:
        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await query.message.edit_text(f'Имя: {userbot.firstname}\n\n№ {this_page_number}/{max_page_number}', reply_markup=ikb_sure_reset_firstname)
        await NewFirstname.page_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_firstname_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_firstname_cancel', state=NewFirstname.page_number)
async def btn_firstname_cancel_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.finish()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_firstname_cancel_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_firstname_ok_reset', state=NewFirstname.page_number)
async def btn_firstname_ok_reset_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        await state.update_data(page_number=this_page_number)
        await NewFirstname.new_firstname.set()
        await bot.send_message(query.from_user.id, 'Введите новое имя юзербота')
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_firstname_ok_reset_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.message_handler(state=NewFirstname.new_firstname)
async def take_new_firstname(message: types.Message, state: FSMContext):
    try:
        new_firstname = message.text

        userbots = await db_users.get_userbots(int(message.from_user.id))
        data = await state.get_data()
        this_page_number = data.get('page_number')

        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_firstname(userbot.telegram_id, new_firstname)
        await bot.send_message(userbot.telegram_id, f'update_firstname @::@ {new_firstname}')

        new_profile = await create_userbot_profile(message.from_user.id, this_page_number)

        await bot.send_message(message.from_user.id, new_profile, reply_markup=ikb_manage_userbots)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_new_firstname', 'error', message.from_user.id, message.from_user.first_name, error)


# lastname
@dp.callback_query_handler(text_contains='btn_reset_lastname')
async def btn_reset_lastname_pressed(query: types.CallbackQuery):
    try:
        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await query.message.edit_text(f'Имя: {userbot.firstname}\n\n№ {this_page_number}/{max_page_number}', reply_markup=ikb_sure_reset_lastname)
        await NewLastname.page_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_lastname', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_lastname_cancel', state=NewLastname.page_number)
async def btn_lastname_cancel_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.finish()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_lastname_cancel_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_lastname_ok_reset', state=NewLastname.page_number)
async def btn_firstname_ok_reset_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        await state.update_data(page_number=this_page_number)
        await NewLastname.new_lastname.set()
        await bot.send_message(query.from_user.id, 'Введите новую фамилию юзербота')
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_firstname_ok_reset_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.message_handler(state=NewLastname.new_lastname)
async def take_new_firstname(message: types.Message, state: FSMContext):
    try:
        new_lastname = message.text

        userbots = await db_users.get_userbots(int(message.from_user.id))
        data = await state.get_data()
        this_page_number = data.get('page_number')

        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_lastname(userbot.telegram_id, new_lastname)
        await bot.send_message(userbot.telegram_id, f'update_lastname @::@ {new_lastname}')

        new_profile = await create_userbot_profile(message.from_user.id, this_page_number)

        await bot.send_message(message.from_user.id, new_profile, reply_markup=ikb_manage_userbots)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_new_firstname', 'error', message.from_user.id, message.from_user.first_name, error)


# bio
@dp.callback_query_handler(text_contains='btn_reset_bio')
async def btn_reset_bio_pressed(query: types.CallbackQuery):
    try:
        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await query.message.edit_text(f'Bio: {userbot.firstname}\n\n№ {this_page_number}/{max_page_number}', reply_markup=ikb_sure_reset_bio)
        await NewBio.page_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_bio', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_bio_cancel', state=NewBio.page_number)
async def btn_bio_cancel_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.finish()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_bio_cancel_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_bio_ok_reset', state=NewBio.page_number)
async def btn_firstname_ok_reset_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        await state.update_data(page_number=this_page_number)
        await NewBio.new_bio.set()
        await bot.send_message(query.from_user.id, 'Введите новое bio юзербота')
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_firstname_ok_reset_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.message_handler(state=NewBio.new_bio)
async def take_new_firstname(message: types.Message, state: FSMContext):
    try:
        new_bio = message.text

        userbots = await db_users.get_userbots(int(message.from_user.id))
        data = await state.get_data()
        this_page_number = data.get('page_number')

        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_bio(userbot.telegram_id, new_bio)
        await bot.send_message(userbot.telegram_id, f'update_bio @::@ {new_bio}')

        new_profile = await create_userbot_profile(message.from_user.id, this_page_number)

        await bot.send_message(message.from_user.id, new_profile, reply_markup=ikb_manage_userbots)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_new_firstname', 'error', message.from_user.id, message.from_user.first_name, error)


# Sex
@dp.callback_query_handler(text_contains='btn_reset_sex')
async def btn_reset_sex_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_reset_sex)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_sex', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_sex_')
async def btn_sex_pressed(query: types.CallbackQuery):
    try:
        new_sex = query.data.split('_')[-1]

        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_sex(userbot.telegram_id, new_sex)

        new_profile = await create_userbot_profile(query.from_user.id, this_page_number)

        await query.message.edit_text(new_profile, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_sex', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# Age
@dp.callback_query_handler(text_contains='btn_reset_age')
async def btn_reset_age_pressed(query: types.CallbackQuery):
    try:
        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await query.message.edit_text(f'Текущий возраст - {userbot.age}\n\n№ {this_page_number}/{max_page_number}', reply_markup=ikb_sure_reset_age)
        await NewAge.page_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_age', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_cancel', state=NewAge.page_number)
async def btn_cancel_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.finish()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_cancel_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_ok_reset_age', state=NewAge.page_number)
async def btn_ok_reset_age_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        await state.update_data(page_number=this_page_number)
        await NewAge.new_age.set()
        await bot.send_message(query.from_user.id, 'Введите новый возраст юзербота. Ваше сообщение должно содержать одно число (от 1 до 100)')
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_ok_reset_age', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.message_handler(state=NewAge.new_age)
async def take_new_age(message: types.Message, state: FSMContext):
    try:
        new_age = message.text
        try_new_age = int(new_age)

        if not 1 <= try_new_age <= 100:
            await bot.send_message(message.from_user.id,
                                   'Число должно находиться в интервале от 1 до 100')
            return

        userbots = await db_users.get_userbots(int(message.from_user.id))
        data = await state.get_data()
        this_page_number = data.get('page_number')

        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_age(userbot.telegram_id, new_age)

        new_profile = await create_userbot_profile(message.from_user.id, this_page_number)

        await bot.send_message(message.from_user.id, new_profile, reply_markup=ikb_manage_userbots)
        await state.finish()
    except ValueError as error:
        await message.answer('Введите одно число (от 1 до 100)\nНапример: 24')
        await log_all('take_new_age', 'warning', message.from_user.id, message.from_user.first_name, error)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_new_age', 'error', message.from_user.id, message.from_user.first_name, error)


# use_emoji
@dp.callback_query_handler(text_contains='btn_reset_use_emoji')
async def btn_reset_use_emoji_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_reset_use_emoji)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_use_emoji_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_use_emoji_')
async def btn_use_emoji_pressed(query: types.CallbackQuery):
    try:
        new_value = int(query.data.split('_')[-1])

        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_use_emoji(userbot.telegram_id, new_value)

        new_profile = await create_userbot_profile(query.from_user.id, this_page_number)

        await query.message.edit_text(new_profile, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_use_emoji_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# gpt_task
@dp.callback_query_handler(text_contains='btn_reset_gpt_task')
async def btn_reset_gpt_task_pressed(query: types.CallbackQuery):
    try:
        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await query.message.edit_text(f'Текущая задача GPT - {userbot.gpt_task}\n\n№ {this_page_number}/{max_page_number}', reply_markup=ikb_sure_reset_gpt_task)
        await NewGptTask.page_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_gpt_task_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_gpt_task_cancel', state=NewGptTask.page_number)
async def btn_gpt_task_cancel_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.finish()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_gpt_task_cancel_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_gpt_task_ok_reset', state=NewGptTask.page_number)
async def btn_gpt_task_ok_reset_pressed(query: types.CallbackQuery, state: FSMContext):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        await state.update_data(page_number=this_page_number)
        await NewGptTask.new_gpt_task.set()
        await bot.send_message(query.from_user.id, 'Введите новый текст задачи к ChatGPT')
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_gpt_task_ok_reset_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.message_handler(state=NewGptTask.new_gpt_task)
async def take_new_gpt_task(message: types.Message, state: FSMContext):
    try:
        userbots = await db_users.get_userbots(int(message.from_user.id))
        data = await state.get_data()
        this_page_number = data.get('page_number')

        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_gpt_task(userbot.telegram_id, message.text)

        new_profile = await create_userbot_profile(message.from_user.id, this_page_number)

        await bot.send_message(message.from_user.id, new_profile, reply_markup=ikb_manage_userbots)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_new_gpt_task', 'error', message.from_user.id, message.from_user.first_name, error)


# commenting_posts
@dp.callback_query_handler(text_contains='btn_reset_commenting_posts')
async def btn_reset_commenting_posts_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_reset_commenting_posts)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_commenting_posts_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_commenting_posts_')
async def btn_commenting_posts_pressed(query: types.CallbackQuery):
    try:
        new_value = int(query.data.split('_')[-1])

        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_commenting_posts(userbot.telegram_id, new_value)

        new_profile = await create_userbot_profile(query.from_user.id, this_page_number)

        await query.message.edit_text(new_profile, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_commenting_posts_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# chat_in_comments
@dp.callback_query_handler(text_contains='btn_reset_chat_in_comments')
async def btn_reset_chat_in_comments_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_reset_chat_in_comments)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_chat_in_comments_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_chat_in_comments_')
async def btn_commenting_posts_pressed(query: types.CallbackQuery):
    try:
        new_value = int(query.data.split('_')[-1])

        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_chat_in_comments(userbot.telegram_id, new_value)

        new_profile = await create_userbot_profile(query.from_user.id, this_page_number)

        await query.message.edit_text(new_profile, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_commenting_posts_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# chat_in_groups
@dp.callback_query_handler(text_contains='btn_reset_chat_in_groups')
async def btn_reset_chat_in_groups_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_reply_markup(ikb_reset_chat_in_groups)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_reset_chat_in_groups_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_chat_in_groups_')
async def btn_chat_in_groups_pressed(query: types.CallbackQuery):
    try:
        new_value = int(query.data.split('_')[-1])

        userbots = await db_users.get_userbots(int(query.from_user.id))
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        userbot_id = userbots[this_page_number - 1]
        userbot = await db_userbots.select_userbot(int(userbot_id))

        await db_userbots.reset_chat_in_groups(userbot.telegram_id, new_value)

        new_profile = await create_userbot_profile(query.from_user.id, this_page_number)

        await query.message.edit_text(new_profile, reply_markup=ikb_manage_userbots)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_chat_in_groups_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


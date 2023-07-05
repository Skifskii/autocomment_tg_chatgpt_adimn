from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import ikb_buy, ikb_subscribe
from loader import dp, bot
from utils.db_api.quick_commands import user as db_users
from utils.yookassa_api.new_payment import create_new_payment, check_payment_status

from data.config import subscriptions_dict, subscription_prices
from data.texts import profile_answer, buy_no_email_answer, select_subscription_message, \
    choose_subscription_type_answer, \
    unknown_error_answer, payment_link_message, invalid_email_value_type
from logs.log_all import log_all
from states import Buy


@dp.message_handler(commands='profile')
async def command_profile(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        user_subscription = subscriptions_dict[user.status]
        await message.answer(profile_answer.format(user_name=user.firstname, user_subscription=user_subscription), reply_markup=ikb_buy)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('profile', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_buy')
async def btn_buy_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_text(select_subscription_message, reply_markup=ikb_subscribe)
        await Buy.subscription.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_buy_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_back', state=Buy.subscription)
async def select_subscription_messages_back(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.finish()


@dp.callback_query_handler(text_contains='btn_subscribe', state=Buy.subscription)
async def choose_subscription_type(query: types.CallbackQuery, state: FSMContext):
    try:
        subscription_type = query.data.split('_')[-1]
        await state.update_data(subscription=subscription_type)
        await query.message.edit_text(buy_no_email_answer)
        await Buy.email.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('choose_subscription_type', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=Buy.email)
async def check_email(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        subscription_type = data.get('subscription')
        # await db_users.set_email(message.from_user.id, message.text)
        #
        user = await db_users.select_user(message.from_user.id)
        payment_data = await create_new_payment(subscription_prices[subscription_type],
                                                subscriptions_dict[subscription_type], message.text)

        await message.answer(
            payment_link_message.format(payment_link=payment_data["confirmation"]["confirmation_url"]))
        await state.finish()
        is_successful = await check_payment_status(payment_data, user)
        if is_successful:
            await db_users.set_status(message.from_user.id, subscription_type)
            await db_users.set_date_subscription_finish(message.from_user.id, str((date.today() + timedelta(days=30))))
            await message.answer(
                choose_subscription_type_answer.format(subscription_type=subscriptions_dict[subscription_type]))
            await log_all('choose_subscription_type', 'info', user.user_id, user.firstname,
                          f'Subscribed {subscriptions_dict[subscription_type]}')
        else:
            await message.answer(unknown_error_answer)
            await log_all('choose_subscription_type', 'info', user.user_id, user.firstname,
                          f'Failed attempt to subscribe {subscriptions_dict[subscription_type]}')
        await state.finish()
    except ValueError as error:
        await message.answer(invalid_email_value_type)
        await log_all('check_email', 'error', message.from_user.id, message.from_user.first_name, error)
        await message.answer(select_subscription_message, reply_markup=ikb_subscribe)
        await Buy.subscription.set()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('check_email', 'error', message.from_user.id, message.from_user.first_name, error)
        await state.finish()

from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import ikb_subscribe, ikb_manage_groups
from loader import dp, bot
from utils.db_api.quick_commands import user as db_users
from utils.yookassa_api.new_payment import create_new_payment, check_payment_status

from data.config import subscriptions_dict, subscription_prices
from data.texts import profile_answer, buy_no_email_answer, select_subscription_message, \
    choose_subscription_type_answer, \
    unknown_error_answer, payment_link_message, invalid_email_value_type, groups_empty, add_group_message, \
    group_added_message, group_list_message, input_group_to_delete_number_message, group_deleted_message, \
    userbots_list_message
from logs.log_all import log_all
from states import AddGroup, DeleteGroup


@dp.message_handler(commands='my_userbots')
async def command_my_userbots(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        user_userbots = user.userbots

        # if user_groups == '':
        #     await message.answer(groups_empty, reply_markup=ikb_manage_groups)
        #     return

        l_userbot_list = user_userbots.split(' @@ ; @@ ')[1:]
        userbot_id, userbot_username, userbot_firstname, userbot_lastname = l_userbot_list[0].split(' @@ , @@ ')
        s_userbot_info = f'1) {userbot_firstname} {userbot_lastname}'
        await message.answer(userbots_list_message.format(userbots_list=s_userbot_info))
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('command_my_userbots', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_add')
async def btn_add_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_text(add_group_message)
        await AddGroup.group_info.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_add_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=AddGroup.group_info)
async def take_group_info(message: types.Message, state: FSMContext):
    try:
        group_name, group_link = message.text.split('\n')
        await db_users.add_group(message.from_user.id, group_name + ' @@ , @@ ' + group_link)

        await message.answer(group_added_message)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_group_info', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_delete')
async def btn_delete_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_text(query.message.text + '\n\n' + input_group_to_delete_number_message)
        await DeleteGroup.group_number.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_add_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=DeleteGroup.group_number)
async def delete_group_by_number(message: types.Message, state: FSMContext):
    try:
        group_number = int(message.text)

        user = await db_users.select_user(message.from_user.id)
        user_groups = user.groups
        if user_groups == '':
            await message.answer(groups_empty, reply_markup=ikb_manage_groups)
            return
        l_group_list = user_groups.split(' @@ ; @@ ')[1:]
        l_group_list.pop(group_number - 1)
        await db_users.delete_groups(message.from_user.id)
        for group in l_group_list:
            await db_users.add_group(message.from_user.id, group)

        await message.answer(group_deleted_message)
        await state.finish()
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('take_group_info', 'error', message.from_user.id, message.from_user.first_name, error)


# @dp.callback_query_handler(text_contains='btn_subscribe', state=Buy.subscription)
# async def choose_subscription_type(query: types.CallbackQuery, state: FSMContext):
#     try:
#         subscription_type = query.data.split('_')[-1]
#         await state.update_data(subscription=subscription_type)
#         await query.message.edit_text(buy_no_email_answer)
#         await Buy.email.set()
#     except Exception as error:
#         await query.message.answer(unknown_error_answer)
#         await log_all('choose_subscription_type', 'error', query.message.from_user.id, query.message.from_user.first_name, error)
#
#
# @dp.message_handler(state=Buy.email)
# async def check_email(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#         subscription_type = data.get('subscription')
#         # await db_users.set_email(message.from_user.id, message.text)
#         #
#         user = await db_users.select_user(message.from_user.id)
#         payment_data = await create_new_payment(subscription_prices[subscription_type],
#                                                 subscriptions_dict[subscription_type], message.text)
#
#         await message.answer(
#             payment_link_message.format(payment_link=payment_data["confirmation"]["confirmation_url"]))
#         await state.finish()
#         is_successful = await check_payment_status(payment_data, user)
#         if is_successful:
#             await db_users.set_status(message.from_user.id, subscription_type)
#             await db_users.set_date_subscription_finish(message.from_user.id, str((date.today() + timedelta(days=30))))
#             await message.answer(
#                 choose_subscription_type_answer.format(subscription_type=subscriptions_dict[subscription_type]))
#             await log_all('choose_subscription_type', 'info', user.user_id, user.firstname,
#                           f'Subscribed {subscriptions_dict[subscription_type]}')
#         else:
#             await message.answer(unknown_error_answer)
#             await log_all('choose_subscription_type', 'info', user.user_id, user.firstname,
#                           f'Failed attempt to subscribe {subscriptions_dict[subscription_type]}')
#         await state.finish()
#     except ValueError as error:
#         await message.answer(invalid_email_value_type)
#         await log_all('check_email', 'error', message.from_user.id, message.from_user.first_name, error)
#         await message.answer(select_subscription_message, reply_markup=ikb_subscribe)
#         await Buy.subscription.set()
#     except Exception as error:
#         await message.answer(unknown_error_answer)
#         await log_all('check_email', 'error', message.from_user.id, message.from_user.first_name, error)
#         await state.finish()

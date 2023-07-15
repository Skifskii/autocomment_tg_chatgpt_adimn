from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import ikb_manage_channels, ikb_add
from loader import dp
from utils.db_api.quick_commands import user as db_users
from data.texts import unknown_error_answer, invalid_channel_number_answer, channels_list_is_empty_message, \
    channels_list_message, add_channel_message, channel_added_message, input_channel_to_delete_number_message, \
    channel_deleted_message
from logs.log_all import log_all
from states import AddChannel, DeleteChannel


async def create_channels_list(user_id, page_number: int = 1) -> str:
    channels = await db_users.get_channels(user_id)

    right_border = page_number * 10
    right_border = min(right_border, len(channels))
    if right_border % 10 == 0:
        left_border = right_border - 10
    else:
        left_border = (right_border // 10) * 10

    s_channels_list = ''
    for channel_number in range(left_border, right_border):
        s_channels_list += f'{channel_number + 1}) {channels[channel_number]}\n'

    def round_top_to_tens(x):
        if x % 10 == 0:
            return x // 10
        return x // 10 + 1

    answer = channels_list_message.format(channels_list=s_channels_list,
                                          page_number=page_number,
                                          total_number_of_pages=round_top_to_tens(len(channels)))
    return answer

@dp.message_handler(commands='my_channels')
async def command_my_channels(message: types.Message):
    try:
        channels = await db_users.get_channels(message.from_user.id)
        if not channels:
            await message.answer(channels_list_is_empty_message, reply_markup=ikb_add)
            return

        channels_list = await create_channels_list(message.from_user.id)
        await message.answer(channels_list, reply_markup=ikb_manage_channels)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('command_my_channels', 'error', message.from_user.id, message.from_user.first_name, error)


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

        new_page = await create_channels_list(query.from_user.id, page_number=new_page_number)
        await query.message.edit_text(new_page, reply_markup=ikb_manage_channels)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_move_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_left')
async def btn_right_pressed(query: types.CallbackQuery):
    try:
        this_page_number, max_page_number = map(int, query.message.text.split('\n')[-1].split(' ')[-1].split('/'))
        if this_page_number < max_page_number:
            new_page = await create_channels_list(query.from_user.id, page_number=this_page_number + 1)
            await query.message.edit_text(new_page, reply_markup=ikb_manage_channels)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_right_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='btn_add')
async def btn_add_pressed(query: types.CallbackQuery):
    try:
        await query.message.edit_text(add_channel_message)
        await AddChannel.channel_info.set()
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_add_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


@dp.message_handler(state=AddChannel.channel_info)
async def get_channels(message: types.Message, state: FSMContext):
    try:
        channels = message.text.split('\n')
        for channel in channels:
            channel = channel.replace('https://t.me/', '')
            if not channel.startswith('@'):
                channel = '@' + channel
            await db_users.add_channel(message.from_user.id, channel)

        await message.answer(channel_added_message)
        await state.finish()
        await command_my_channels(message)
    except Exception as error:
        await log_all('take_channel_info', 'error', message.from_user.id, message.from_user.first_name, error)
        await state.finish()


# @dp.callback_query_handler(text_contains='btn_delete')
# async def btn_delete_pressed(query: types.CallbackQuery):
#     try:
#         await query.message.edit_text(query.message.text + '\n\n' + input_channel_to_delete_number_message)
#         await DeleteChannel.channel_number.set()
#     except Exception as error:
#         await query.message.answer(unknown_error_answer)
#         await log_all('btn_add_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)


# @dp.message_handler(state=DeleteChannel.channel_number)
# async def delete_channel_by_number(message: types.Message, state: FSMContext):
#     try:
#         channel_number = int(message.text)
#
#         user_channels = await db_users.get_channels(message.from_user.id)
#         if user_channels == '':
#             await message.answer(channels_list_is_empty, reply_markup=ikb_manage_channels)
#             return
#         l_channel_list = user_channels.split(' @@ ; @@ ')[1:]
#         l_channel_list.pop(channel_number - 1)
#         await db_users.delete_channel(message.from_user.id)
#         for channel in l_channel_list:
#             await db_users.add_channel(message.from_user.id, channel)
#
#         await message.answer(channel_deleted_message)
#         await state.finish()
#     except ValueError as error:
#         await message.answer(invalid_channel_number_answer)
#         await log_all('take_channel_info', 'error', message.from_user.id, message.from_user.first_name, str(error) + ' ' + str(type(error)))
#         await state.finish()
#     except Exception as error:
#         await message.answer(unknown_error_answer)
#         await log_all('take_channel_info', 'error', message.from_user.id, message.from_user.first_name, error)
#         await state.finish()

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

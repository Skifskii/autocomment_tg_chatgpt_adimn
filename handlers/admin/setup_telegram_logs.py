from aiogram import types

from keyboards.inline import ikb_telegram_logs_permissions
from loader import dp, bot
from utils.db_api.quick_commands import user as db_users
from utils.db_api.quick_commands import telegram_log_permission as db_tgperms

from data.texts import unknown_error_answer, telegram_logs_permission_symbols
from logs.log_all import log_all


@dp.message_handler(commands='setup_telegram_logs')
async def setup_telegram_logs(message: types.Message):
    try:
        user = await db_users.select_user(message.from_user.id)
        if user.status != 'admin':
            return
        statuses = (await db_tgperms.select_permissions())[0]
        await bot.send_message(message.from_user.id,
                               f'{telegram_logs_permission_symbols[statuses.info]} Info\n{telegram_logs_permission_symbols[statuses.warning]} Warning\n{telegram_logs_permission_symbols[statuses.error]} Error',
                               reply_markup=ikb_telegram_logs_permissions)
    except Exception as error:
        await message.answer(unknown_error_answer)
        await log_all('setup_telegram_logs', 'error', message.from_user.id, message.from_user.first_name, error)


@dp.callback_query_handler(text_contains='change_perm')
async def tglog_messages(query: types.CallbackQuery):
    try:
        current_text = query.message.text
        row_index = -1
        rows_list = current_text.split('\n')
        if query.data == 'change_perm_info':
            row_index = 0
        if query.data == 'change_perm_warning':
            row_index = 1
        if rows_list[row_index].startswith('✅'):
            new_perm = '❌'
        else:
            new_perm = '✅'
        current_text = current_text.replace(rows_list[row_index], f'{new_perm} {rows_list[row_index][2:]}')
        await query.message.edit_text(current_text, reply_markup=ikb_telegram_logs_permissions)
    except Exception as error:
        await query.message.answer(unknown_error_answer)
        await log_all('btn_buy_pressed', 'error', query.message.from_user.id, query.message.from_user.first_name, error)

@dp.callback_query_handler(text_contains='btn_back')
async def tglog_messages_back(query: types.CallbackQuery):
    finish_text = query.message.text
    new_statuses = []
    for status in finish_text.split('\n'):
        if status.startswith('✅'):
            new_statuses.append(1)
        else:
            new_statuses.append(0)
    await db_tgperms.reset_permissions(new_statuses)
    await bot.delete_message(query.message.chat.id, query.message.message_id)

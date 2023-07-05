from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_telegram_logs_permissions = InlineKeyboardMarkup(row_width=1)

btn_info = InlineKeyboardButton(text='Info', callback_data='change_perm_info')
ikb_telegram_logs_permissions.insert(btn_info)

btn_warning = InlineKeyboardButton(text='Warning', callback_data='change_perm_warning')
ikb_telegram_logs_permissions.insert(btn_warning)

btn_error = InlineKeyboardButton(text='Error', callback_data='change_perm_error')
ikb_telegram_logs_permissions.insert(btn_error)

btn_back = InlineKeyboardButton(text='🔙', callback_data='btn_back')
ikb_telegram_logs_permissions.insert(btn_back)

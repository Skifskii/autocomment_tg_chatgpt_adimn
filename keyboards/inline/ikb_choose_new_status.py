from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_choose_new_status = InlineKeyboardMarkup(row_width=2)

btn_status_gpt = InlineKeyboardButton(text='GPT', callback_data='btn_status_gpt')
ikb_choose_new_status.insert(btn_status_gpt)

btn_status_vip = InlineKeyboardButton(text='VIP', callback_data='btn_status_vip')
ikb_choose_new_status.insert(btn_status_vip)

btn_status_user = InlineKeyboardButton(text='user', callback_data='btn_status_user')
ikb_choose_new_status.insert(btn_status_user)

btn_status_admin = InlineKeyboardButton(text='admin', callback_data='btn_status_admin')
ikb_choose_new_status.insert(btn_status_admin)

btn_status_ban = InlineKeyboardButton(text='Ban user', callback_data='btn_status_ban')
ikb_choose_new_status.insert(btn_status_ban)

btn_back = InlineKeyboardButton(text='🔙 Отмена', callback_data='btn_back')
ikb_choose_new_status.insert(btn_back)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_manage_userbots = InlineKeyboardMarkup(row_width=2)

btn_left = InlineKeyboardButton(text='<-', callback_data='btn_move_userbots_left')
ikb_manage_userbots.insert(btn_left)

btn_right = InlineKeyboardButton(text='->', callback_data='btn_move_userbots_right')
ikb_manage_userbots.insert(btn_right)

btn_edit = InlineKeyboardButton(text='Изменить', callback_data='btn_edit')
ikb_manage_userbots.insert(btn_edit)

btn_common_settings = InlineKeyboardButton(text='Общие настройки', callback_data='btn_common_settings')
ikb_manage_userbots.insert(btn_common_settings)

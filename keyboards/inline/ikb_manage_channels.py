from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_manage_channels = InlineKeyboardMarkup(row_width=2)

btn_left = InlineKeyboardButton(text='<-', callback_data='btn_move_left')
ikb_manage_channels.insert(btn_left)

btn_right = InlineKeyboardButton(text='->', callback_data='btn_move_right')
ikb_manage_channels.insert(btn_right)

btn_add = InlineKeyboardButton(text='Добавить', callback_data='btn_add')
ikb_manage_channels.insert(btn_add)

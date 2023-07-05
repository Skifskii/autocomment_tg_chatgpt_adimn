from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_manage_groups = InlineKeyboardMarkup()

btn_delete = InlineKeyboardButton(text='Удалить', callback_data='btn_delete')
ikb_manage_groups.insert(btn_delete)

btn_add = InlineKeyboardButton(text='Добавить', callback_data='btn_add')
ikb_manage_groups.insert(btn_add)

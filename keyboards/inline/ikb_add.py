from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_add = InlineKeyboardMarkup()

btn_add = InlineKeyboardButton(text='Добавить', callback_data='btn_add')
ikb_add.insert(btn_add)

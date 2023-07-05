from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_subscribe = InlineKeyboardMarkup(row_width=2)

btn_subscribe_gpt = InlineKeyboardButton(text='GPT', callback_data='btn_subscribe_gpt')
ikb_subscribe.insert(btn_subscribe_gpt)

btn_subscribe_vip = InlineKeyboardButton(text='VIP', callback_data='btn_subscribe_vip')
ikb_subscribe.insert(btn_subscribe_vip)

btn_back = InlineKeyboardButton(text='🔙 Отмена', callback_data='btn_back')
ikb_subscribe.insert(btn_back)

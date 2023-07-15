from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_chat_in_groups = InlineKeyboardMarkup(row_width=2)

btn_chat_in_groups_0 = InlineKeyboardButton(text='❌ Нет', callback_data='btn_chat_in_groups_0')
ikb_reset_chat_in_groups.insert(btn_chat_in_groups_0)

btn_chat_in_groups_1 = InlineKeyboardButton(text='✅ Да', callback_data='btn_chat_in_groups_1')
ikb_reset_chat_in_groups.insert(btn_chat_in_groups_1)

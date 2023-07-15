from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_chat_in_comments = InlineKeyboardMarkup(row_width=2)

btn_chat_in_comments_0 = InlineKeyboardButton(text='❌ Нет', callback_data='btn_chat_in_comments_0')
ikb_reset_chat_in_comments.insert(btn_chat_in_comments_0)

btn_chat_in_comments_1 = InlineKeyboardButton(text='✅ Да', callback_data='btn_chat_in_comments_1')
ikb_reset_chat_in_comments.insert(btn_chat_in_comments_1)

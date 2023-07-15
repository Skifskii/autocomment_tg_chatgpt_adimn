from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_commenting_posts = InlineKeyboardMarkup(row_width=2)

btn_commenting_posts_0 = InlineKeyboardButton(text='❌ Нет', callback_data='btn_commenting_posts_0')
ikb_reset_commenting_posts.insert(btn_commenting_posts_0)

btn_commenting_posts_1 = InlineKeyboardButton(text='✅ Да', callback_data='btn_commenting_posts_1')
ikb_reset_commenting_posts.insert(btn_commenting_posts_1)

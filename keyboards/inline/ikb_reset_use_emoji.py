from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_use_emoji = InlineKeyboardMarkup(row_width=2)

btn_no = InlineKeyboardButton(text='❌ Нет', callback_data='btn_use_emoji_0')
ikb_reset_use_emoji.insert(btn_no)

btn_yes = InlineKeyboardButton(text='✅ Да', callback_data='btn_use_emoji_1')
ikb_reset_use_emoji.insert(btn_yes)

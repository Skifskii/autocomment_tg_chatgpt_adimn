from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_add_keywords = InlineKeyboardMarkup()

btn_cancel_keywords = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_keywords_cancel')
ikb_add_keywords.insert(btn_cancel_keywords)

btn_add_keywords = InlineKeyboardButton(text='Изменить', callback_data='btn_keywords_add')
ikb_add_keywords.insert(btn_add_keywords)

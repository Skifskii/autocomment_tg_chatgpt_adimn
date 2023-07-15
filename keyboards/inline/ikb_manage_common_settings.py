from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_manage_common_settings = InlineKeyboardMarkup(row_width=1)

btn_reset_delay_answer = InlineKeyboardButton(text='Задержка подписок', callback_data='btn_reset_delay_subscribe')
ikb_manage_common_settings.insert(btn_reset_delay_answer)

btn_reset_delay_answer = InlineKeyboardButton(text='Задержка ответов', callback_data='btn_reset_delay_answer')
ikb_manage_common_settings.insert(btn_reset_delay_answer)

btn_reset_keywords = InlineKeyboardButton(text='Ключевые слова', callback_data='btn_reset_keywords')
ikb_manage_common_settings.insert(btn_reset_keywords)

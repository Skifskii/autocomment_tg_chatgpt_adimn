from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_common_settings = InlineKeyboardMarkup()

btn_reset_common_settings = InlineKeyboardButton(text='Изменить', callback_data='btn_reset_common_settings')
ikb_reset_common_settings.insert(btn_reset_common_settings)

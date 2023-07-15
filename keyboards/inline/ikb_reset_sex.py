from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_reset_sex = InlineKeyboardMarkup(row_width=2)

btn_sex_m = InlineKeyboardButton(text='М', callback_data='btn_sex_m')
ikb_reset_sex.insert(btn_sex_m)

btn_sex_f = InlineKeyboardButton(text='Ж', callback_data='btn_sex_f')
ikb_reset_sex.insert(btn_sex_f)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_age = InlineKeyboardMarkup(row_width=2)

btn_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_cancel')
ikb_sure_reset_age.insert(btn_cancel)

btn_ok_reset_age = InlineKeyboardButton(text='Изменить', callback_data='btn_ok_reset_age')
ikb_sure_reset_age.insert(btn_ok_reset_age)

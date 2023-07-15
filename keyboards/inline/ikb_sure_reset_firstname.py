from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_firstname = InlineKeyboardMarkup(row_width=2)

btn_firstname_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_firstname_cancel')
ikb_sure_reset_firstname.insert(btn_firstname_cancel)

btn_firstname_ok_reset = InlineKeyboardButton(text='Изменить', callback_data='btn_firstname_ok_reset')
ikb_sure_reset_firstname.insert(btn_firstname_ok_reset)

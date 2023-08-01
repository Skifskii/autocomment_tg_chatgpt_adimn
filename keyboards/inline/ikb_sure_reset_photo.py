from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_photo = InlineKeyboardMarkup(row_width=2)

btn_photo_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_photo_cancel')
ikb_sure_reset_photo.insert(btn_photo_cancel)

btn_photo_ok_reset = InlineKeyboardButton(text='Изменить', callback_data='btn_photo_ok_reset')
ikb_sure_reset_photo.insert(btn_photo_ok_reset)

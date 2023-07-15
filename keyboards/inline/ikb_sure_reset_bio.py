from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_bio = InlineKeyboardMarkup(row_width=2)

btn_bio_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_bio_cancel')
ikb_sure_reset_bio.insert(btn_bio_cancel)

btn_bio_ok_reset = InlineKeyboardButton(text='Изменить', callback_data='btn_bio_ok_reset')
ikb_sure_reset_bio.insert(btn_bio_ok_reset)

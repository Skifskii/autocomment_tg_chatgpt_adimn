s = """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_lastname = InlineKeyboardMarkup(row_width=2)

btn_lastname_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_lastname_cancel')
ikb_sure_reset_lastname.insert(btn_lastname_cancel)

btn_lastname_ok_reset = InlineKeyboardButton(text='Изменить', callback_data='btn_lastname_ok_reset')
ikb_sure_reset_lastname.insert(btn_lastname_ok_reset)

"""

print(s.replace('lastname', 'bio').replace('Lastname', 'Bio'))

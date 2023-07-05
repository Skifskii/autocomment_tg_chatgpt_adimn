from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_actions_with_user = InlineKeyboardMarkup(row_width=2)

btn_change_status = InlineKeyboardButton(text='Изменить статус', callback_data='btn_change_status')
ikb_actions_with_user.insert(btn_change_status)

btn_send_message = InlineKeyboardButton(text='Отправить сообщение', callback_data='btn_send_message')
ikb_actions_with_user.insert(btn_send_message)

btn_back = InlineKeyboardButton(text='🔙 Отмена', callback_data='btn_back')
ikb_actions_with_user.insert(btn_back)

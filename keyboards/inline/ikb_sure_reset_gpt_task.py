from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_sure_reset_gpt_task = InlineKeyboardMarkup(row_width=2)

btn_gpt_task_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='btn_gpt_task_cancel')
ikb_sure_reset_gpt_task.insert(btn_gpt_task_cancel)

btn_gpt_task_ok_reset = InlineKeyboardButton(text='Изменить', callback_data='btn_gpt_task_ok_reset')
ikb_sure_reset_gpt_task.insert(btn_gpt_task_ok_reset)

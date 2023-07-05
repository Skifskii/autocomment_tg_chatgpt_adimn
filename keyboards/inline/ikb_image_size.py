from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_image_size = InlineKeyboardMarkup()

btn_size_256 = InlineKeyboardButton(text='Низкое', callback_data='btn_size_256')
ikb_image_size.insert(btn_size_256)

btn_size_512 = InlineKeyboardButton(text='Среднее', callback_data='btn_size_512')
ikb_image_size.insert(btn_size_512)

btn_size_1024 = InlineKeyboardButton(text='Высокое', callback_data='btn_size_1024')
ikb_image_size.insert(btn_size_1024)

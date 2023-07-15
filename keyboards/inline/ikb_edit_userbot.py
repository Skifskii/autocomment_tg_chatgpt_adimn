from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_edit_userbot = InlineKeyboardMarkup(row_width=2)

btn_reset_firstname = InlineKeyboardButton(text='Имя', callback_data='btn_reset_firstname')
ikb_edit_userbot.insert(btn_reset_firstname)

btn_reset_lastname = InlineKeyboardButton(text='Фамилия', callback_data='btn_reset_lastname')
ikb_edit_userbot.insert(btn_reset_lastname)

btn_reset_bio = InlineKeyboardButton(text='bio', callback_data='btn_reset_bio')
ikb_edit_userbot.insert(btn_reset_bio)

btn_reset_sex = InlineKeyboardButton(text='Пол', callback_data='btn_reset_sex')
ikb_edit_userbot.insert(btn_reset_sex)

btn_reset_age = InlineKeyboardButton(text='Возраст', callback_data='btn_reset_age')
ikb_edit_userbot.insert(btn_reset_age)

btn_reset_use_emoji = InlineKeyboardButton(text='Использование эмодзи', callback_data='btn_reset_use_emoji')
ikb_edit_userbot.insert(btn_reset_use_emoji)

btn_reset_gpt_task = InlineKeyboardButton(text='Задача GPT', callback_data='btn_reset_gpt_task')
ikb_edit_userbot.insert(btn_reset_gpt_task)

btn_reset_commenting_posts = InlineKeyboardButton(text='Комментирование постов', callback_data='btn_reset_commenting_posts')
ikb_edit_userbot.insert(btn_reset_commenting_posts)

btn_reset_chat_in_comments = InlineKeyboardButton(text='Общение в комментариях', callback_data='btn_reset_chat_in_comments')
ikb_edit_userbot.insert(btn_reset_chat_in_comments)

btn_reset_chat_in_groups = InlineKeyboardButton(text='Общение в группах', callback_data='btn_reset_chat_in_groups')
ikb_edit_userbot.insert(btn_reset_chat_in_groups)

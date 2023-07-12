from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Начать работу'),
        types.BotCommand('my_channels', 'Мои каналы'),
        types.BotCommand('my_userbots', 'Мои юзерботы'),
        types.BotCommand('start_userbots', 'Начать автокомментинг')


        # types.BotCommand('help', 'Помощь'),
        # types.BotCommand('forget', 'Очистить память'),
        # types.BotCommand('image', 'Сгенерировать изображение'),
        # types.BotCommand('profile', 'Профиль')
    ])

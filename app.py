async def on_startup_app(dp):
    from loader import db
    from utils.db_api.db_gino import on_startup_db
    await on_startup_db(dp)
    await db.gino.create_all()

    from logs.logging_loguru.logger import logger
    logger.info('Bot started')

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup_app, skip_updates=False)

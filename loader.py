import openai
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from yookassa import Configuration

from utils.db_api.db_gino import db
from data import config

Configuration.account_id = config.SHOP_ID
Configuration.secret_key = config.SHOP_API_TOKEN

openai.api_key = config.OPENAI_API_KEY
bot = Bot(token=config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']

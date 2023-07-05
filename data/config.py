import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAM_TOKEN = str(os.getenv('TELEGRAM_TOKEN'))

PG_HOST = str(os.getenv('PG_HOST'))
PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
PG_DATABASE = str(os.getenv('PG_DATABASE'))
POSTGRES_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

SHOP_ID = os.getenv("SHOP_ID")
SHOP_API_TOKEN = os.getenv("SHOP_API_TOKEN")

subscriptions_dict = {
    'user': 'Нет подписки',
    'gpt': 'GPT',
    'vip': 'VIP',
    'admin': 'Admin'
}

subscription_prices = {
    'gpt': 100,
    'vip': 250
}

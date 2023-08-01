from aiogram.dispatcher.filters.state import StatesGroup, State


class NewOpenaiApiKey(StatesGroup):
    new_openai_api_key = State()

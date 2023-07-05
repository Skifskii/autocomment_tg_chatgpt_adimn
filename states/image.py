from aiogram.dispatcher.filters.state import StatesGroup, State


class Image(StatesGroup):
    prompt = State()
    translated_prompt = State()
    size = State()

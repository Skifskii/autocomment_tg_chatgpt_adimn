from aiogram.dispatcher.filters.state import StatesGroup, State


class TakeNewKeywords(StatesGroup):
    new_data = State()

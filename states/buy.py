from aiogram.dispatcher.filters.state import StatesGroup, State


class Buy(StatesGroup):
    email = State()
    subscription = State()

from aiogram.dispatcher.filters.state import StatesGroup, State


class NewProxy(StatesGroup):
    new_proxy = State()

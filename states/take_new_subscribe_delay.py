from aiogram.dispatcher.filters.state import StatesGroup, State


class TakeNewSubscribeData(StatesGroup):
    new_data = State()

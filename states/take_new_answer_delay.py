from aiogram.dispatcher.filters.state import StatesGroup, State


class TakeNewAnswerData(StatesGroup):
    new_data = State()

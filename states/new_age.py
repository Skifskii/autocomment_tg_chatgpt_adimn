from aiogram.dispatcher.filters.state import StatesGroup, State


class NewAge(StatesGroup):
    new_age = State()
    page_number = State()

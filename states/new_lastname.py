from aiogram.dispatcher.filters.state import StatesGroup, State


class NewLastname(StatesGroup):
    new_lastname = State()
    page_number = State()

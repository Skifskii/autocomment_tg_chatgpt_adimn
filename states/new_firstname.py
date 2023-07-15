from aiogram.dispatcher.filters.state import StatesGroup, State


class NewFirstname(StatesGroup):
    new_firstname = State()
    page_number = State()

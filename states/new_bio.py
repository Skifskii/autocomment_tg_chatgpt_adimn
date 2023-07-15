from aiogram.dispatcher.filters.state import StatesGroup, State


class NewBio(StatesGroup):
    new_bio = State()
    page_number = State()

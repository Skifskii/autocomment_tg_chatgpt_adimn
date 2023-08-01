from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPhoto(StatesGroup):
    new_photo = State()
    page_number = State()

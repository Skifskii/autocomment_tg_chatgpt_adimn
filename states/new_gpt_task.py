from aiogram.dispatcher.filters.state import StatesGroup, State


class NewGptTask(StatesGroup):
    new_gpt_task = State()
    page_number = State()

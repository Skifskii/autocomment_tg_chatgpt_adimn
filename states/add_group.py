from aiogram.dispatcher.filters.state import StatesGroup, State


class AddGroup(StatesGroup):
    group_info = State()

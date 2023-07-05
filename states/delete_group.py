from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteGroup(StatesGroup):
    group_number = State()

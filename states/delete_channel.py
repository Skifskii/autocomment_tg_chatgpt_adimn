from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteChannel(StatesGroup):
    channel_number = State()

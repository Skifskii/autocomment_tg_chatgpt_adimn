from aiogram.dispatcher.filters.state import StatesGroup, State


class AddChannel(StatesGroup):
    channel_info = State()
    page = State()

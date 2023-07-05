from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectUser(StatesGroup):
    user_id = State()
    status = State()
    select_new_status = State()
    message_to_user = State()

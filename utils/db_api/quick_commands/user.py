from asyncpg import UniqueViolationError
import json

from logs.log_all import log_all
from utils.db_api.schemas.user import User


# ---------- User ----------
async def add_user(user_id: int, username: str, firstname: str, lastname: str):
    try:
        user = User(user_id=user_id, username=username, firstname=firstname, lastname=lastname)
        await user.create()
    except UniqueViolationError as error:
        await log_all('add_user', 'error', user_id, firstname, f'User did not added: {error}')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def get_channels(user_id):
    user = await select_user(user_id)
    channels = user.channels
    if channels == '':
        return []
    return channels.split(', ')


async def add_channel(user_id, new_channel):
    user = await select_user(user_id)
    if user.channels == '':
        await user.update(channels = new_channel).apply()
        return
    await user.update(channels=user.channels + ', ' + new_channel).apply()


async def delete_channel(user_id):
    user = await select_user(user_id)
    await user.update(groups='').apply()


async def get_userbots(user_id):
    user = await select_user(user_id)
    json_userbots = user.userbots
    dict_userbots = json.loads(json_userbots)
    return dict_userbots['userbots']


async def set_email(user_id, email):
    user = await select_user(user_id)
    await user.update(email=email).apply()


async def get_email(user_id):
    user = await select_user(user_id)
    return user.email


async def clear_story(user_id):
    user = await select_user(user_id)
    await user.update(chat_story='{"messages":[]}').apply()


async def set_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()


async def commit_new_message(user_id):
    user = await select_user(user_id)
    await user.update(total_messages_sent=user.total_messages_sent + 1).apply()


async def commit_new_image(user_id):
    user = await select_user(user_id)
    await user.update(total_images_generated=user.total_images_generated + 1).apply()


async def set_user_status_for_all():
    users = await select_all_users()
    for user in users:
        await user.update(status='user', total_images_generated=0, total_messages_sent=0).apply()


async def set_date_subscription_finish(user_id, date):
    user = await select_user(user_id)
    await user.update(date_subscription_finish=date).apply()


async def set_username(user_id, username):
    user = await select_user(user_id)
    await user.update(username=username).apply()

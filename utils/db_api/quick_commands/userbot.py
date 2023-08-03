from asyncpg import UniqueViolationError

from logs.log_all import log_all
from utils.db_api.schemas.userbot import Userbot


async def select_all_userbots():
    userbots = await Userbot.query.gino.all()
    return userbots


async def select_userbot(telegram_id) -> Userbot:
    userbot = await Userbot.query.where(Userbot.telegram_id == telegram_id).gino.first()
    return userbot


async def add_userbot(telegram_id: int):
    try:
        userbot = Userbot(telegram_id=telegram_id)
        await userbot.create()
    except UniqueViolationError as error:
        await log_all('add_user', 'error', telegram_id, f'User did not added: {error}')


async def reset_phone(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(phone=new_value).apply()


async def reset_firstname(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(firstname=new_value).apply()


async def reset_lastname(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(lastname=new_value).apply()


async def reset_bio(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(bio=new_value).apply()


async def reset_sex(telegram_id: int, new_sex: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(sex=new_sex).apply()


async def reset_age(telegram_id: int, new_age: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(age=new_age).apply()


async def reset_use_emoji(telegram_id: int, new_use_emoji: int):
    userbot = await select_userbot(telegram_id)
    await userbot.update(use_emoji=new_use_emoji).apply()


async def reset_gpt_task(telegram_id: int, new_gpt_task: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(gpt_task=new_gpt_task).apply()


async def reset_commenting_posts(telegram_id: int, new_commenting_posts: int):
    userbot = await select_userbot(telegram_id)
    await userbot.update(commenting_posts=new_commenting_posts).apply()


async def reset_chat_in_comments(telegram_id: int, new_chat_in_comments: int):
    userbot = await select_userbot(telegram_id)
    await userbot.update(chat_in_comments=new_chat_in_comments).apply()


async def reset_chat_in_groups(telegram_id: int, new_chat_in_groups: int):
    userbot = await select_userbot(telegram_id)
    await userbot.update(chat_in_groups=new_chat_in_groups).apply()


async def reset_proxy(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(proxy_data=new_value).apply()


async def reset_owner_id(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(owner_id=new_value).apply()


async def reset_alive(telegram_id: int, new_value: str):
    userbot = await select_userbot(telegram_id)
    await userbot.update(alive=new_value).apply()


# async def test():
#     await db.set_bind(data.config.POSTGRES_URI)
#     await db.gino.create_all()
#     print(await select_userbot(1))


# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())

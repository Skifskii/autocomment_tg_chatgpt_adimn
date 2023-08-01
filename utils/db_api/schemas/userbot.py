from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, BigInteger, String, sql, Integer, VARCHAR


class Userbot(BaseModel):
    __tablename__ = 'userbots'
    telegram_id = Column(BigInteger, primary_key=True, nullable=False)
    phone = Column(String(64), default='')
    password = Column(String(64), default='')
    api_id = Column(BigInteger, default=2040)
    owner_id = Column(BigInteger, default=-1)
    api_hash = Column(String(64), default='b18441a1ff607e10a989891a5462e627')
    firstname = Column(String(64), default='')
    lastname = Column(String(64), default='')
    bio = Column(String(70), default='')
    sex = Column(String(64), default='m')
    age = Column(String(64), default='20')
    gpt_task = Column(String, default='ты играешь роль комментатора постов в социальных сетях. Пиши короткие комментарии, высказывая свое мнение по теме поста или соглашаясь с автором. Используй сленг. Пиши так, будто общаешься с друзьями.')
    use_emoji = Column(Integer, default=0)
    commenting_posts = Column(Integer, default=0)
    chat_in_comments = Column(Integer, default=0)
    chat_in_groups = Column(Integer, default=0)
    proxy_data = Column(String, default='')

    query: sql.select

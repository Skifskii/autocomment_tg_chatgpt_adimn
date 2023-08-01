from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, BigInteger, String, sql, Integer, VARCHAR


class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(64), default='')
    firstname = Column(String(64), default='')
    lastname = Column(String(64), default='')
    channels = Column(String, default='')
    userbots = Column(String, default='')
    email = Column(String, default='')
    status = Column(VARCHAR, default='user')
    date_subscription_finish = Column(String, default='')
    keywords = Column(String, default='')
    answer_delay = Column(Integer, default=10)
    subscribe_delay = Column(Integer, default=60)

    query: sql.select

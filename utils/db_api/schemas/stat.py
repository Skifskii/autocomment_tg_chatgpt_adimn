from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, String, sql, Integer


class EverydayStats(BaseModel):
    __tablename__ = 'stat'
    num_of_alive_userbots = Column(Integer, primary_key=True, default=0)

    query: sql.select

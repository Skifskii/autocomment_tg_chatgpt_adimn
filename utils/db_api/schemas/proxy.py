from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, String, sql, Integer


class Proxy(BaseModel):
    __tablename__ = 'proxies'
    proxy_data = Column(String, primary_key=True, nullable=False)
    accounts_number = Column(Integer, default=0)

    query: sql.select

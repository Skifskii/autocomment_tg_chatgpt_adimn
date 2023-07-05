from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, sql, Integer


class TelegramLogPermission(BaseModel):
    __tablename__ = 'tg_log_permissions'
    info = Column(Integer, primary_key=True, default=0)
    warning = Column(Integer, default=0)
    error = Column(Integer, default=0)

    query: sql.select

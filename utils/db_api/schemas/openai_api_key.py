from utils.db_api.db_gino import BaseModel
from sqlalchemy import Column, String, sql, Integer


class OpeanaiApiKey(BaseModel):
    __tablename__ = 'openai_api_keys'
    key = Column(String, primary_key=True, nullable=False)

    query: sql.select

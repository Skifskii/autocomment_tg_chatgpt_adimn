from utils.db_api.db_gino import db


async def rebuild_tables():
    await db.gino.drop_all()
    await db.gino.create_all()

# Тут будут запросы к моделям sqlalchemy
from database import DB

async def select_user(async_session):
  from sqlalchemy import text
  # Select User
  user_stmt = text("select * from public.user")
  async with async_session as session, session.begin():
    result = await session.execute(user_stmt)
    usr = result.scalars()
    print(usr)

async def test_connection():
  session = DB.get_session()
  await select_user(session)


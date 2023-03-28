import asyncio
# from controller.cli_controller import ChatBotControllerCLI
import logging
from database import DB

# получаем тут единый пул подключений к базе из database
# отдаем это подключение контроллеру, который уже отдает его модели, которая отдает его ДАО, который использует его для запросов к базе

# try:
#   bot = ChatBotControllerCLI()
#   bot.handle_message("/selectusers")
# except Exception as e:
#   logging.exception(e)


async def select_user(async_session):
  print(async_session, type(async_session))
  from sqlalchemy import text
  # Select User
  user_stmt = text("select * from public.user")
  async with async_session as session, session.begin():
    result = await session.execute(user_stmt)
    usr = result.scalars()
    for u in usr:
      print(u)

async def main():
  global DB
  DB = await DB.init_db() # getting DB

  await select_user(DB.get_session())

  # for AsyncEngine created in function scope, close and
  # clean-up pooled connections
  await DB.engine.dispose()

if __name__ == "__main__":
  asyncio.run(main())
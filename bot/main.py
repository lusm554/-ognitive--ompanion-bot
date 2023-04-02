import asyncio
# from controller.cli_controller import ChatBotControllerCLI
import logging
from database import DB

# try:
#   bot = ChatBotControllerCLI()
#   bot.handle_message("/selectusers")
# except Exception as e:
#   logging.exception(e)


async def select_user(async_session):
  from sqlalchemy import text
  # Select User
  user_stmt = text("select * from public.user")
  async with async_session as session, session.begin():
    result = await session.execute(user_stmt)
    usr = result.scalars()
    print(usr)

async def main():
  global DB
  instance_db = await DB.init_db() # setting up tables 
  await select_user(DB.get_session())

  # ONLY FOR TESTING SINGLETON CLASS, DON'T USE THIS SHIT IN OTHER CASES!
  from dao import test_connection
  await test_connection()

  # for AsyncEngine created in function scope, close and
  # clean-up pooled connections
  await instance_db.engine.dispose()

if __name__ == "__main__":
  asyncio.run(main())
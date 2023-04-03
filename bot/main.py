import asyncio
from database import DB
from config import TelegramConfig
from telegramfront import telegram_main

async def main():
  global DB
  # instance_db = await DB.init_db() # setting up tables 
  # for AsyncEngine created in function scope, close and
  # clean-up pooled connections
  # await instance_db.engine.dispose()

  # running telegram bot
  await telegram_main(TelegramConfig.TELEGRAM_TOKEN)

if __name__ == "__main__":
  telegram_main()
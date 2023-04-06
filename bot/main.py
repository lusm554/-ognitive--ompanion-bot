import asyncio
from database import DB
from config import TelegramConfig
from telegramfront import telegram_main

async def initdb():
  await DB.init_db()

async def main():
  # global DB

  # running telegram bot
  telegram_application = telegram_main(TelegramConfig.TELEGRAM_TOKEN)
  telegram_application.bot_data["controller"] = 1 # init here controller for bot command handlers

  # starting bot in separate task
  bot_task = asyncio.create_task(telegram_application.run_polling())
  # starting the database initialization in a separate task
  db_task  = asyncio.create_task(initdb())

  # wait for both tasks to complete
  await asyncio.gather(bot_task, db_task)

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()

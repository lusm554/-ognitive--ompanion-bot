import asyncio
from database import DB
from config import TelegramConfig
from telegramfront import telegram_main
from dao import UserDAO


async def infinite_loop():
  try:
    while 1:
      await asyncio.sleep(1)
  except (KeyboardInterrupt, SystemExit):
    pass

async def initdb(_):
  await DB.init_db()

async def some_task():
  d = UserDAO()
  await d.read()

def main():
  telegram_application = telegram_main(TelegramConfig.TELEGRAM_TOKEN)
  telegram_application.bot_data["controller"] = 1 # init here controller for bot command handlers
  telegram_application.job_queue.run_once(initdb, when=0)
  telegram_application.run_polling()
  # async with telegram_application as application: # Calls `initialize` and `shutdown` 
  #   await application.start()
  #   await application.updater.start_polling()
  #   await initdb()
  #   await some_task()
  #   # here should some ligc that keeps event loop running
  #   await infinite_loop()
  #   await application.updater.stop()
  #   await application.stop()

if __name__ == "__main__":
  main()
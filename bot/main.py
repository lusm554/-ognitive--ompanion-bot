from database import DB
from config import TelegramConfig
from telegramfront import telegram_main
from controller import ChatBotControllerCLI

async def initdb(_):
  await DB.init_db()

def main():
  controller = ChatBotControllerCLI()
  telegram_application = telegram_main(TelegramConfig.TELEGRAM_TOKEN)
  telegram_application.bot_data["controller"] = controller # init here controller for bot command handlers
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
from database import DB
from config import TelegramConfig
from telegramfront import telegram_main
from controller import TelegramController

async def initdb(_):
  await DB.init_db()

def main():
  telegram_application = telegram_main(TelegramConfig.TELEGRAM_TOKEN)
  telegram_application.bot_data.controller = TelegramController()
  telegram_application.job_queue.run_once(initdb, when=0)
  telegram_application.run_polling()

if __name__ == "__main__":
  main()
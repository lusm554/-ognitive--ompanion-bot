from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# TODO: as best practice, add /start, /help commands. Add unknown command handler 
# TODO: add commands to BotFather for menu
# TODO: move CommandHandler to decorator
# TODO: add logging 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Starts an interaction with the user. Adds it to the user database."""
  await update.message.reply_text("Hello! I'm todo bot. See more in menu or by /help command.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Shows a help message, like a short text about what bot can do and a list of commands."""
  await update.message.reply_text("<Here should be help message>")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Tell user about called command does not exist."""
  await update.message.reply_text("This command don't exist. Use menu or /help command for info.")

def main():
  # REMOVE
  import os
  token = os.getenv("TELEGRAM_TOKEN")
  # REMOVE

  application = ApplicationBuilder().token(token).build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  help_handler = CommandHandler('help', help)
  application.add_handler(help_handler)

  # This handler must be added last. If it added before the other handlers, it would be triggered before the CommandHandlers.
  unknown_handler = MessageHandler(filters.COMMAND, unknown)
  application.add_handler(unknown_handler)
   
  application.run_polling()

if __name__ == '__main__':
  main()
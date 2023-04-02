from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# TODO: as best practice, add /start, /help commands. Add unknown command handler 
# TODO: use state machine bot works
# TODO: add commands to BotFather for menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Start command. First command that user send. This command sends greeting message."""
  await update.message.reply_text(text="I'm a bot, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Returns a help message, like a short text about what bot can do and a list of commands."""
  await update.message.reply_text(text="There should be help command.")

async def todolist(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [
      InlineKeyboardButton("Option 1", callback_data="1"),
      InlineKeyboardButton("Option 2", callback_data="2"),
    ],
    [InlineKeyboardButton("Option 3", callback_data="3")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text("Please choose:", reply_markup=reply_markup)

if __name__ == '__main__':
  import os
  token = os.getenv("TELEGRAM_TOKEN")
  application = ApplicationBuilder().token(token).build()
  
  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)
  help_handler = CommandHandler('help', help)
  application.add_handler(help_handler)
  todolist_handler = CommandHandler('todolist', todolist)
  application.add_handler(todolist_handler) 

  application.run_polling()

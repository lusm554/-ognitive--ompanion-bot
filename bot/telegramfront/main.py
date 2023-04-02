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
  """Sends a message with three inline buttons attached."""
  keyboard = [
    [
      InlineKeyboardButton("Option 1", callback_data="1"),
      InlineKeyboardButton("Option 2", callback_data="2"),
    ],
    [InlineKeyboardButton("Option 3", callback_data="3")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query
  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()
  await query.edit_message_text(text=f"Selected option: {query.data}")

def main():
  import os
  token = os.getenv("TELEGRAM_TOKEN")
  application = ApplicationBuilder().token(token).build()
  
  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  help_handler = CommandHandler('help', help)
  application.add_handler(help_handler)

  todolist_handler = CommandHandler('todolist', todolist)
  application.add_handler(todolist_handler) 
  application.add_handler(CallbackQueryHandler(button))

  application.run_polling()

if __name__ == '__main__':
  main()
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
  msg_text = ' '.join(context.args)
  logging.info(f"Received command chat: {msg_text}")
  response = gen_response(msg_text)
  logging.info(f"Response command chat: {response}")
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
  application = ApplicationBuilder().token(token).build()

  start_handler = CommandHandler('start', start)
  chat_handler = CommandHandler('chat', chat)
  application.add_handler(start_handler)
  application.add_handler(chat_handler)

  application.run_polling()

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Cancels and ends the conversation."""
  msg = await context.bot_data.controller.cancel_cmd_handler()
  await update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())
  return ConversationHandler.END
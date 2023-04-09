from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Cancels and ends the conversation."""
  msg = await context.bot_data.controller.cancel_cmd_handler()
  if update.callback_query:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(msg)
  else:
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())
  return ConversationHandler.END
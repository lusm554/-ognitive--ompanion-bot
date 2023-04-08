from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters
from .commonhandlers import cancel

# States of machine of adding task
WAITING_TASK_INPUT_STATE = range(1)

async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Entry point to conversation of adding task."""
  msg = await context.bot_data.controller.initaddtask_cmd_handler()
  await update.message.reply_text(msg)
  return WAITING_TASK_INPUT_STATE

async def handletaskinput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Callback processing input from user for new task."""
  update_message = update.message
  msg = await context.bot_data.controller.addtask_cmd_handler(update_message)
  await update.message.reply_text(msg)
  return ConversationHandler.END

ADDTASK_CONVERSATION_HANDLER = ConversationHandler(
  entry_points=[CommandHandler("addtask", addtask)],
  states={
    WAITING_TASK_INPUT_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), handletaskinput)],
  },
  fallbacks=[CommandHandler("cancel", cancel)],
)
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters
from .commonhandlers import cancel

# States of machine of adding task
WAITING_TASK_INPUT_STATE = range(1)

async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  msg = "Send me the name of the task you want to add.\n\nSend /cancel at any time to stop our convesation."
  await update.message.reply_text(msg)
  return WAITING_TASK_INPUT_STATE

async def handletaskinput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  new_task_name = update.message.text
  # OPERATION ON ADDING TASK HERE
  # new_task_id = max(map(int, [*TASKS.keys(), 0]))+1
  # TASKS[str(new_task_id)] = {
  #   "name": new_task_name,
  #   "id": str(new_task_id)
  # }
  msg = f"Your task `{new_task_name}` added.\n\nSee it through /listtasks."
  await update.message.reply_text(msg)
  return ConversationHandler.END

ADDTASK_CONVERSATION_HANDLER = ConversationHandler(
  entry_points=[CommandHandler("addtask", addtask)],
  states={
    WAITING_TASK_INPUT_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), handletaskinput)],
  },
  fallbacks=[CommandHandler("cancel", cancel)],
)
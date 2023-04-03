import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
  Application,
  CallbackQueryHandler,
  MessageHandler,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
  filters
)

# Enable logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# TODO: add name of task in last, ended operation

# States of machine of adding task
WAITING_TASK_INPUT_STATE = range(1)

# States of machine of tasks list
ALL_TASKS_STATE, PARTICULAR_TASK_STATE, EDIT_TASK_STATE = range(3)

# TEMP STORE TASK BEFORE EDITING
# TODO: find better solution for this. For example make state GLOBAL
TASK4EDITING = None

TASKS = {
  "1": {
    "name": "Оформить подписку",
    "id": "1"
  },
  # "2": {
  #   "name": "Купить продукты на ужин",
  #   "id": "2"
  # },
  # "3": {
  #   "name": "Сдать реферат",
  #   "id": "3"
  # },
}

# TODO: Consider returning keyboard with keys DONE and CONTINUE after end states like `complete`, `delete` etc.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Starts an interaction with the user. Adds it to the user database."""
  logger.info("Someone run start command.")
  await update.message.reply_text("Hello! Now bot active.")

async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  msg = "Send me the name of the task you want to add.\n\nSend /cancel at any time to stop our convesation."
  logger.info("Start command addtask")
  await update.message.reply_text(msg)
  return WAITING_TASK_INPUT_STATE

async def handletaskinput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  new_task_name = update.message.text
  new_task_id = max(map(int, [*TASKS.keys(), 0]))+1
  TASKS[str(new_task_id)] = {
    "name": new_task_name,
    "id": str(new_task_id)
  }
  msg = f"Your task `{new_task_name}` added.\n\nSee it through /listtasks."
  await update.message.reply_text(msg)
  logger.info(f"Added new task {new_task_name}")
  return ConversationHandler.END

def get_start_keyboard():
  pagination = [
    InlineKeyboardButton(text="Next page", callback_data="next"),
    InlineKeyboardButton(text="Previous page", callback_data="prev"),
  ]
  keyboard_menu = [
    *[[InlineKeyboardButton(text=task["name"], callback_data=task["id"])] for task in TASKS.values()],
    pagination if len(TASKS) > 10 else [] # using pagination if tasks more than 10
  ]
  keyboard = InlineKeyboardMarkup(keyboard_menu)
  return keyboard

async def listtasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Starts a conversation and shows the task to the user. Also manages pagination if necessary."""
  reply_markup = get_start_keyboard()
  msg = "Your list of tasks. Click on one of them to continue.\n\nSend /cancel at any time to stop our convesation."
  if update.callback_query: # Prompt same text & keyboard as `listtasks` does but not as new message
    query = update.callback_query
    await query.answer()
    logger.info("Continue conversation from start, sends tasks list.")
    await query.edit_message_text(msg, reply_markup=reply_markup)
  else:
    logger.info("Starting conversation, sends tasks list.")
    await update.message.reply_text(msg, reply_markup=reply_markup)
  return ALL_TASKS_STATE

async def task_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Handles a click on a task. Shows task interaction buttons to the user."""
  logger.info("User clicked task button. Shows task operations.")
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data
  selected_task = TASKS.get(selected_task_id)
  keyboard_menu = [
    # [InlineKeyboardButton(text=selected_task["name"], callback_data=selected_task["id"])],
    [
      InlineKeyboardButton(text="Back", callback_data="back"+selected_task_id),
      InlineKeyboardButton(text="Complete", callback_data="complete"+selected_task_id),
      InlineKeyboardButton(text="Edit", callback_data="edit"+selected_task_id),
      InlineKeyboardButton(text="Delete", callback_data="delete"+selected_task_id),
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard_menu)
  await query.edit_message_text(
    text=f"{selected_task['name']}", reply_markup=reply_markup
  )
  return PARTICULAR_TASK_STATE

async def task_complete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Closes the user's task."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("complete"):]
  # logic of closing task here
  del TASKS[selected_task_id]
  await query.edit_message_text(text=f"Your task closed.")
  logger.info("Users completed task. Conversation ended.")
  return ConversationHandler.END

async def task_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Deletes the user's task."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("delete"):]
  # logic of deleting task here
  del TASKS[selected_task_id]
  await query.edit_message_text(text=f"Your task deleted.")
  logger.info("Users deleted task. Conversation ended.")
  return ConversationHandler.END

async def task_request_edit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Requests new name of the user's task."""
  global TASK4EDITING
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("edit"):]
  TASK4EDITING = TASKS.get(selected_task_id) 
  await query.edit_message_text(text=f"Send me new name of task `{TASK4EDITING['name']}`.")
  logger.info("User request editing task.")
  return EDIT_TASK_STATE

async def task_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Edits name of the user's task."""
  global TASK4EDITING
  new_name = update.message.text
  TASKS[TASK4EDITING["id"]]["name"] = new_name
  await update.message.reply_text(f"The name of task changed from `{TASK4EDITING['name']}` to `{new_name}`.")
  TASK4EDITING = None
  logger.info("User edited task. Conversation ended.")
  return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Cancels and ends the conversation."""
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  await update.message.reply_text(
    "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
  )
  return ConversationHandler.END

def main() -> None:
  """Run the bot."""
  # Create the Application and pass it your bot's token.
  import os
  token = os.getenv("TELEGRAM_TOKEN") 
  application = Application.builder().token(token).build()

  addtask_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("addtask", addtask)],
    states={
      WAITING_TASK_INPUT_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), handletaskinput)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
  )
  application.add_handler(addtask_conversation_handler)

  listtasks_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("listtasks", listtasks)],
    states={
      ALL_TASKS_STATE: [CallbackQueryHandler(task_button_callback)], # todo: add here pagination callbacks
      PARTICULAR_TASK_STATE: [
        CallbackQueryHandler(listtasks, pattern="^" + "back" + "*"),
        CallbackQueryHandler(task_complete_callback, pattern="^" + "complete" + "*"), # re: starts from "back"
        CallbackQueryHandler(task_delete_callback, pattern="^" + "delete" + "*"), # re: starts from "back"
        CallbackQueryHandler(task_request_edit_callback, pattern="^" + "edit" + "*"), # re: starts from "back"
      ],
      EDIT_TASK_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), task_edit)]
      # START_ROUTES: [
      #     CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
      #     CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
      #     CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
      #     CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
      # ],
      # END_ROUTES: [
      #     CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
      #     CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
      # ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
  )
  application.add_handler(listtasks_conversation_handler)

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  # Run the bot until the user presses Ctrl-C
  application.run_polling()


if __name__ == "__main__":
  main()

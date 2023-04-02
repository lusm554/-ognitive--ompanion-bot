import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
  Application,
  CallbackQueryHandler,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
)

# Enable logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# States of machine
LIST_TASKS, PARTICULAR_TASK, END = range(3)

TASKS = [
  {
    "name": "Оформить подписку",
    "id": "1"
  },
  {
    "name": "Купить продукты на ужин",
    "id": "2"
  },
  {
    "name": "Сдать реферат",
    "id": "3"
  },
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Starts an interaction with the user. Adds it to the user database."""
  logger.info("Someone run start command.")
  await update.message.reply_text("Hello! Now bot active.")

async def commandnotfound(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Starts an interaction with the user. Adds it to the user database."""
  logger.info("Command not found.")
  await update.message.reply_text("Command not found.")

async def todolist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Starts a conversation and shows the task to the user. Also manages pagination if necessary."""
  pagination = [
    InlineKeyboardButton(text="Next page", callback_data="next"),
    InlineKeyboardButton(text="Previous page", callback_data="prev"),
  ]
  keyboard_menu = [
    *[[InlineKeyboardButton(text=task["name"], callback_data=task["id"])] for task in TASKS],
    pagination if len(TASKS) > 10 else [] # using pagination if tasks more than 10
  ]
  reply_markup = InlineKeyboardMarkup(keyboard_menu)
  msg = "Your list of tasks. Click on one of them to continue.\n\nSend /cancel at any time to stop our convesation."
  if update.callback_query: # Prompt same text & keyboard as `todolist` does but not as new message
    query = update.callback_query
    await query.answer()
    logger.info("Continue conversation from start, sends tasks list.")
    await query.edit_message_text(msg, reply_markup=reply_markup)
  else:
    logger.info("Starting conversation, sends tasks list.")
    await update.message.reply_text(msg, reply_markup=reply_markup)
  return LIST_TASKS

async def task_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Handles a click on a task. Shows task interaction buttons to the user."""
  logger.info("User clicked task button. Shows task operations.")
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data
  selected_task = list(filter(lambda tsk: str(tsk["id"]) == selected_task_id, TASKS))[0]
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
  return PARTICULAR_TASK

async def task_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Returns users to previous state, to list of tasks."""
  logger.info("running task_back_callback")
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  await query.edit_message_text(text=f"Back to list of tasks for: {query.data}")
  return LIST_TASKS
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

  conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("todolist", todolist)],
    states={
      LIST_TASKS: [CallbackQueryHandler(task_button_callback)], # todo: add here pagination callbacks
      PARTICULAR_TASK: [
        CallbackQueryHandler(todolist, pattern="^" + "back" + "*"),
        CallbackQueryHandler(task_back_callback), # re: starts from "back"
      ]
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
  application.add_handler(conversation_handler)

  # todolistt_handler = CommandHandler('todolist', todolist)
  # application.add_handler(todolistt_handler)

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  # Run the bot until the user presses Ctrl-C
  application.run_polling()


if __name__ == "__main__":
  main()

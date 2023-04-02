import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
  await update.message.reply_text("Hello! Now bot active.")  

async def todolist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  keyboard_menu = [
    *[[InlineKeyboardButton(text=task["name"], callback_data="1"+task["id"])] for task in TASKS]
    # add keys for pagination
  ]
  reply_markup = InlineKeyboardMarkup(keyboard_menu)
  await update.message.reply_text("Your todo list:", reply_markup=reply_markup)
  return LIST_TASKS

async def task_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  # await query.edit_message_text(text=f"Selected option: {query.data}")
  await query.answer()
  selected_task_id = query.data[1:]
  selected_task = list(filter(lambda tsk: str(tsk["id"]) == selected_task_id, TASKS))[0]
  keyboard_menu = [
    [InlineKeyboardButton(text=selected_task["name"], callback_data="2"+selected_task["id"])],
    [
      InlineKeyboardButton(text="Edit", callback_data="2"+"edit"),
      InlineKeyboardButton(text="Delete", callback_data="2"+"deleta"),
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard_menu)
  await query.edit_message_text(
    text="Operations on specific task:", reply_markup=reply_markup
  )
  return PARTICULAR_TASK

async def task_operations_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()
  await query.edit_message_text(text=f"Selected option: {query.data}")
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
      LIST_TASKS: [CallbackQueryHandler(task_button_callback, pattern="^" + str(1) + "*")],
      PARTICULAR_TASK: [CallbackQueryHandler(task_operations_callback, pattern="^" + str(2) + "*")]
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
    fallbacks=[CommandHandler("start", start)],
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

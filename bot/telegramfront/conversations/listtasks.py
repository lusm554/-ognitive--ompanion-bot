from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
  CallbackQueryHandler,
  MessageHandler,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
  filters
)
import json
from .commonhandlers import cancel

# TODO: add paggination for tasks list
# TODO: add cancle button to list of tasks
# TODO: proper handle errors in serialization/deserialization

# States of machine of tasks list
ALL_TASKS_STATE, PARTICULAR_TASK_STATE, AFTERACTION_TASK_STATE, EDIT_TASK_STATE = range(4)

def serializetask(task: dict) -> str:
  """Serializes task dict to json for for transport over the network."""
  try:
    _task = {
      "id": str(task["id"]),
      "name": task["name"]
    }
    serialized = json.dumps(_task, ensure_ascii=False) # ensure_ascii=False - don't escape non-ASCII characters. Using for ru language.
    return serialized
  except Exception as error:
    raise Exception("Error while seralize task obj.") from error

def deserializetask(task: str) -> dict:
  """Deserializes task json to dict for using like py object."""
  try:
    _task = json.loads(task)
    return _task
  except Exception as error:
    raise Exception("Error while deserialize task obj.") from error

def get_start_keyboard(list_of_tasks):
  keyboard_menu = [
    *[
      [InlineKeyboardButton(text=task["name"], callback_data=serializetask(task))] # using [button] to indicate that there is only one button in this `row`
      for task in list_of_tasks
    ],
  ]
  keyboard = InlineKeyboardMarkup(keyboard_menu)
  return keyboard

def get_afteraction_keyboard():
  keyboard_menu = [
    [
      InlineKeyboardButton(text="Back to tasks", callback_data="back"),
      InlineKeyboardButton(text="We done", callback_data="cancel"),
    ]
  ]
  keyboard = InlineKeyboardMarkup(keyboard_menu)
  return keyboard

async def listtasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Starts a conversation and shows the task to the user. Also manages pagination if necessary."""
  user = (update.callback_query or update.message).from_user # think it's not the best practice.
  msg, list_of_tasks = await context.bot_data.controller.listtasks_cmd_handler(user)
  reply_markup = get_start_keyboard(list_of_tasks)
  if update.callback_query: # Prompt same text & keyboard as `listtasks` does but not as new message
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(msg, reply_markup=reply_markup)
  else:
    await update.message.reply_text(msg, reply_markup=reply_markup)
  if len(list_of_tasks) == 0:
    return ConversationHandler.END
  return ALL_TASKS_STATE

async def task_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Handles a click on a task. Shows task interaction buttons to the user."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  serializedtask = query.data
  selected_task_obj = deserializetask(serializedtask)
  selected_task_id = selected_task_obj["id"]
  keyboard_menu = [
    [
      InlineKeyboardButton(text="Back", callback_data="back"+selected_task_id),
      InlineKeyboardButton(text="Complete", callback_data="complete"+selected_task_id),
      InlineKeyboardButton(text="Edit", callback_data="edit"+selected_task_id),
      InlineKeyboardButton(text="Delete", callback_data="delete"+selected_task_id),
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard_menu)
  msg = await context.bot_data.controller.taskbutton_cmd_handler(selected_task_obj["name"])
  await query.edit_message_text(text=msg, reply_markup=reply_markup)
  return PARTICULAR_TASK_STATE

async def task_complete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Closes the user's task."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("complete"):]
  msg = await context.bot_data.controller.closetask_cmd_handler(selected_task_id)
  keyboard_menu = get_afteraction_keyboard()
  await query.edit_message_text(text=msg, reply_markup=keyboard_menu)
  return AFTERACTION_TASK_STATE

async def task_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Deletes the user's task."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("delete"):]
  msg = await context.bot_data.controller.deletetask_cmd_handler(selected_task_id) 
  keyboard_menu = get_afteraction_keyboard()
  await query.edit_message_text(text=msg, reply_markup=keyboard_menu)
  return AFTERACTION_TASK_STATE

async def task_request_edit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Requests new name of the user's task."""
  query = update.callback_query
  await query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed. Some clients may have trouble otherwise.
  selected_task_id = query.data[len("edit"):]
  msg, task_obj = await context.bot_data.controller.request_taskedit_cmd_handler(selected_task_id)
  context.user_data["edit_task_obj"] = task_obj
  await query.edit_message_text(text=msg)
  return EDIT_TASK_STATE

async def task_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Edits name of the user's task."""
  global TASK4EDITING
  new_name = update.message.text
  selected_task = context.user_data["edit_task_obj"]
  msg = await context.bot_data.controller.taskedit_cmd_handler(selected_task["id"], new_name, selected_task["name"])
  context.user_data["edit_task_id"] = None
  keyboard_menu = get_afteraction_keyboard()
  await update.message.reply_text(msg, reply_markup=keyboard_menu)
  return AFTERACTION_TASK_STATE

LISTTASKS_CONVERSATION_HANDLER = ConversationHandler(
  entry_points=[CommandHandler("listtasks", listtasks)],
  states={
    ALL_TASKS_STATE: [CallbackQueryHandler(task_button_callback)], # todo: add here pagination callbacks
    PARTICULAR_TASK_STATE: [
      CallbackQueryHandler(listtasks, pattern="^" + "back" + "*"),
      CallbackQueryHandler(task_complete_callback, pattern="^" + "complete" + "*"), # re: starts from "back"
      CallbackQueryHandler(task_delete_callback, pattern="^" + "delete" + "*"), # re: starts from "back"
      CallbackQueryHandler(task_request_edit_callback, pattern="^" + "edit" + "*"), # re: starts from "back"
    ],
    EDIT_TASK_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), task_edit)],
    AFTERACTION_TASK_STATE: [
      CallbackQueryHandler(listtasks, pattern="^" + "back" + "*"),
      CallbackQueryHandler(cancel, pattern="^" + "cancel" + "*"),
    ],
  },
  fallbacks=[CommandHandler("cancel", cancel)],
)
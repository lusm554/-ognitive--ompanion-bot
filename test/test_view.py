import pytest
from bot.view.view import View

@pytest.fixture
def bot_view():
  view = View()
  return view

def test_start_msg(bot_view):
  assert bot_view.start_msg() == "Hello! I'm todo bot. See more in menu or by /help command." 

def test_help_msg(bot_view):
  assert bot_view.help_msg() == "<help message>"

def test_unknown_msg(bot_view):
  assert bot_view.unknown_msg() == "This command don't exist. Use menu or /help command for info.\nProbably u may be in action. Use /cancel to stop it."

def test_cancel_msg(bot_view):
  assert bot_view.cancel_msg() == "Bye! I hope we can talk again some day."

def test_start_user_already_exists(bot_view):
  assert bot_view.start_user_already_exists() == "It looks like you are already using the bot."

def test_init_addtask_msg(bot_view):
  assert bot_view.init_addtask_msg() == "Send me the name of the task you want to add.\n\nSend /cancel at any time to stop our convesation."

def test_add_task_msg(bot_view):
  assert bot_view.add_task_msg("new task") == "Your task `new task` added.\n\nSee it through /listtasks."
  assert bot_view.add_task_msg("") == "Your task `` added.\n\nSee it through /listtasks."

def test_list_tasks_msg(bot_view):
  assert bot_view.list_tasks_msg(0) == "You have no tasks. Use /addtask command."
  assert bot_view.list_tasks_msg(1) == "Your list of tasks. Click on one of them to continue.\n\nSend /cancel at any time to stop our convesation."
  assert bot_view.list_tasks_msg(10) == "Your list of tasks. Click on one of them to continue.\n\nSend /cancel at any time to stop our convesation."

def test_taskbutton_msg(bot_view):
  assert bot_view.taskbutton_msg("") == ""
  assert bot_view.taskbutton_msg("new task") == "new task"

def test_close_task_msg(bot_view):
  assert bot_view.close_task_msg("") == "Your task `` closed."
  assert bot_view.close_task_msg("taskname") == "Your task `taskname` closed."

def test_request_taskedit_msg(bot_view):
  assert bot_view.request_taskedit_msg("") == "Send me new name for task ``"
  assert bot_view.request_taskedit_msg("buy food") == "Send me new name for task `buy food`"

def test_taskedit_msg(bot_view):
  assert bot_view.taskedit_msg("", "") == "The name of task changed from `` to ``."
  assert bot_view.taskedit_msg("newname", "") == "The name of task changed from `` to `newname`."
  assert bot_view.taskedit_msg("", "oldname") == "The name of task changed from `oldname` to ``."
  assert bot_view.taskedit_msg("newname", "oldname") == "The name of task changed from `oldname` to `newname`."

def test_deletetask_msg(bot_view):
  assert bot_view.deletetask_msg() == "Your task deleted."

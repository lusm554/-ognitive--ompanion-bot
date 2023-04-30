# Generates output message for commands

class View:
  def __init__(self):
    pass

  def start_msg(self) -> str:
    """Returns message of first interaction with bot."""
    return "Hello! I'm todo bot. See more in menu or by /help command." 
  
  def help_msg(self) -> str:
    """Returns a help message, like a short text about what bot can do and a list of commands."""
    start_cmd = "/start - starts an interaction with the bot\n"
    addtask_cmd = "/addtask - adds task to todo list\n"
    listtasks_cmd = "/listtasks - shows the list of your tasks\n"
    cancel_cmd = "/cancel - cancels the current operation\n"
    help_cmd = "/help - short text about what both can do and a list of commands\n"
    return "The list of tasks:\n" + start_cmd + addtask_cmd + listtasks_cmd + cancel_cmd + help_cmd
  
  def unknown_msg(self) -> str:
    """Returns message about unknown command."""
    return "This command don't exist. Use menu or /help command for info.\nProbably u may be in action. Use /cancel to stop it."
  
  def cancel_msg(self) -> str:
    """Returns message about canceled operation."""
    return "Bye! I hope we can talk again some day."
  
  def start_user_already_exists(self) -> str:
    """Returns a message indicating that the bot is already in use."""
    return "It looks like you are already using the bot."
  
  def init_addtask_msg(self) -> str:
    """Returns message of requesting data for new task."""
    return "Send me the name of the task you want to add.\n\nSend /cancel at any time to stop our convesation."
  
  def add_task_msg(self, taskname: str) -> str:
    """Returns a message of adding new task."""
    return f"Your task `{taskname}` added.\n\nSee it through /listtasks."
  
  def list_tasks_msg(self, tasks_count: int) -> str:
    """Returns message about task list."""
    if tasks_count == 0:
      return "You have no tasks. Use /addtask command."
    return "Your list of tasks. Click on one of them to continue.\n\nSend /cancel at any time to stop our convesation."
  
  def taskbutton_msg(self, taskname: str) -> str:
    return f"{taskname}"
  
  def close_task_msg(self, taskname) -> str:
    """Returns a message about closed task."""
    return f"Your task `{taskname}` closed."
  
  def request_taskedit_msg(self, taskname) -> str:
    """Returns a message about editing task."""
    return f"Send me new name for task `{taskname}`"

  def taskedit_msg(self, new_name, curr_name) -> str:
    """Returns message about edited task."""
    return f"The name of task changed from `{curr_name}` to `{new_name}`."

  def deletetask_msg(self) -> str:
    """Returns message about deleted task."""
    return f"Your task deleted."

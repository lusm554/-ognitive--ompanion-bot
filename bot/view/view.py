# Generates output message for commands

class View:
  def __init__(self):
    pass

  def start_msg(self) -> str:
    """Returns message of first interaction with bot."""
    return "Hello! I'm todo bot. See more in menu or by /help command." 
  
  def start_user_already_exists(self) -> str:
    """Returns a message indicating that the bot is already in use."""
    return "It looks like you are already using the bot."
  
  def add_task_msg(self, taskname: str) -> str:
    """Returns a message of adding new task."""
    return f"Your task `{taskname}` added.\n\nSee it through /listtasks."

# Generates output message for commands

class View:
  def __init__(self):
    pass

  def start_msg(self):
    """Returns message of first interaction with bot."""
    return "Hello! I'm todo bot. See more in menu or by /help command." 
  
  def start_user_already_exists(self):
    """Returns a message indicating that the bot is already in use."""
    return "It looks like you are already using the bot."

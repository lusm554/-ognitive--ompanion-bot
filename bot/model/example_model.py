class ChatBotModel:
  def __init__(self):
    self.commands = ("start", "help", "end")
    self.command_prefix = "/"
    self.state = "inactive"

  def recognize_command(self, message):
    if message in self.commands:
      return message
    return None
  
  def process_message(self, message):
    cmd = self.recognize_command(message)
    if self.state == "inactive":
      if cmd == "start":
        self.state = "active"
        return "Hello! How can I help you?"
      else:
        return "Please start the conversation using the /start command."
    elif self.state == "active":
      if cmd:
        return f"Grats, u run {cmd} command!"
      else:
        return self.ask_question()

  def ask_question(self):
    return "What would you like to know? Type '/help' for the list of available commands."
 

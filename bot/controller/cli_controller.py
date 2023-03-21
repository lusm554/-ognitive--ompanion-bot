from model.cli_model import ChatBotModelCLI
from view.cli_view import ChatBotViewCLI

class ChatBotControllerCLI:
  def __init__(self):
    self.model = ChatBotModelCLI()
    self.view = ChatBotViewCLI()

  def handle_message(self, message):
    response = self.model.process_message(message)
    self.view.display_message(response)
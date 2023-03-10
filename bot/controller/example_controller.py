from model.example_model import ChatBotModel
from view.example_view import ChatBotView

class ChatBotController:
  def __init__(self):
    self.model = ChatBotModel()
    self.view = ChatBotView()

  def handle_message(self, message):
    response = self.model.process_message(message)
    self.view.display_message(response)


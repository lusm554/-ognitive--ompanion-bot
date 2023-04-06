from dao import UserDAO

class ChatBotControllerCLI:
  def __init__(self):
    self.dao = UserDAO()

  async def handle_message(self):
    await self.dao.read()
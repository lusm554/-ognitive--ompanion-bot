# import model - handle data by commands
# import view - generate response message
from model import Model
from view import View
import telegram # for type notations

# connects together mode and view

class TelegramController:
  def __init__(self):
    self.model = Model()
    self.view = View()

  async def start_cmd_handler(self, telegram_user: telegram.User) -> str:
    user_obj = {
      "telegram_id": str(telegram_user.id),
      "first_name": telegram_user.first_name,
      "username": telegram_user.username
    }
    if await self.model.is_user_exist(user_obj["telegram_id"]):
      msg = self.view.start_user_already_exists()
      return msg
    await self.model.add_user(user_obj)
    msg = self.view.start_msg()
    return msg
    
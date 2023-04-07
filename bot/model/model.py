from dao import UserDAO

# Handles data by input commands

class Model:
  def __init__(self):
    self.dao = UserDAO()

  async def add_user(self, user_obj: dict):
    await self.dao.create(user_obj)
  
  async def is_user_exist(self, telegram_id: int):
    user = await self.dao.read(telegram_id)
    return True if user is not None else False 
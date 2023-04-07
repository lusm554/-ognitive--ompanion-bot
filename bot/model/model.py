from dao import UserDAO

# Handles data by input commands

class Model:
  def __init__(self):
    self.dao = UserDAO()

  async def add_user(self, user_obj: dict):
    await self.dao.create(user_obj)
from database import DB
from dao import UserDAO

class ChatBotModelCLI:
  def __init__(self):
    self.db_connection = DB.get_connection()
    self.user_dao = UserDAO(self.db_connection)
    self.commands = ("selectusers")

  def recognize_command(self, msg: str):
    if msg[1:] in self.commands: # msg[1:] - remove "/" char
      return msg[1:]
    return None

  def process_message(self, msg):
    cmd = self.recognize_command(msg)
    if cmd is not None:
      if cmd == "selectusers":
        users = self.select_users()
        return users
    return "Command not found."

  def select_users(self):
    users = self.user_dao.get_users()
    return users
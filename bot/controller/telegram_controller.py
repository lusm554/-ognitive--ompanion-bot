# import model - handle data by commands
# import view - generate response message
from model import UserModel, TaskModel
from view import View
import telegram # for type notations

# connects together mode and view
# TODO: make all operations atomic

class TelegramController:
  def __init__(self):
    self.user_model = UserModel()
    self.task_model = TaskModel()
    self.view = View()

  async def start_cmd_handler(self, telegram_user: telegram.User) -> str:
    """Adds user to database on /start command."""
    user_obj = {
      "telegram_id": str(telegram_user.id),
      "first_name": telegram_user.first_name,
      "username": telegram_user.username
    }
    if await self.user_model.is_user_exist(user_obj["telegram_id"]):
      msg = self.view.start_user_already_exists()
      return msg
    await self.user_model.add_user(user_obj)
    msg = self.view.start_msg()
    return msg
    
  async def addtask_cmd_handler(self, telegram_msg: telegram.Message) -> str:
    """Adds task to database on /addtask command."""
    task_obj = {
      "telegram_user_id": str(telegram_msg.from_user.id),
      "name": telegram_msg.text,
      "status": "todo"
    }
    await self.task_model.add_task(task_obj)
    msg = self.view.add_task_msg(task_obj["name"])
    return msg
  
  async def listtasks_cmd_handler(self, telegram_user: telegram.User) -> list:
    telegram_user_id = str(telegram_user.id)
    tasks = await self.task_model.get_tasks(telegram_user_id)
    tasks = [  # cast from ORM object to python dict
      {"id": task.id, "name": task.name}
      for task in tasks
    ]
    return tasks

  async def closetask_cmd_handler(self, task_id: str) -> str:
    closed_task = await self.task_model.close_task(task_id)
    msg = self.view.close_task_msg(closed_task.name)
    return msg

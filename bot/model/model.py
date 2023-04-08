from dao import UserDAO
from dao import TaskDAO

# Handles data by input commands
# TODO: move the model logic to a separate file

class UserModel:
  def __init__(self):
    self.dao = UserDAO()

  async def add_user(self, user_obj: dict):
    await self.dao.create(user_obj)
  
  async def is_user_exist(self, telegram_id: int):
    user = await self.dao.read(telegram_id)
    return True if user is not None else False

class TaskModel:
  def __init__(self):
    self.dao = TaskDAO()
  
  async def add_task(self, task_obj: dict):
    await self.dao.create(task_obj)

  async def get_tasks(self, telegram_user_id: str) -> list:
    tasks = await self.dao.read(telegram_user_id)
    return tasks
  
  async def get_task(self, task_id: str) -> list:
    task = await self.dao.readone(task_id)
    return task
  
  async def close_task(self, task_id: str):
    task_update_obj = {
      "status": "done"
    }
    closed_task = await self.dao.update(task_id, task_update_obj)
    return closed_task

  async def update_name(self, task_id: str, new_name: str):
    task_update_obj = {
      "name": new_name
    }
    edited_task = await self.dao.update(task_id, task_update_obj)
    return edited_task

  async def delete_task(self, task_id: str):
    deleted_task = await self.dao.delete(task_id)
    return deleted_task
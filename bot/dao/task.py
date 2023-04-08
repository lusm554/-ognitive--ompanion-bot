from .daobase import DAOBase
from database import Task
from sqlalchemy import select

# TODO: it seems not good to use this arch model->dao. where flexibliyu

class TaskDAO(DAOBase):
  def __init__(self):
    super().__init__()
    self.task_model = Task

  async def create(self, data: dict) -> None:
    """Creates record in database of task."""
    async with self.session as session, session.begin():
      task = self.task_model(
        telegram_user_id=data["telegram_user_id"],
        name=data["name"],
        status=data["status"]
      )
      session.add(task)

  async def read(self, key: int):
    pass

  async def update(self, primarykey, data):
    pass

  async def delete(self, primarykey):
    pass
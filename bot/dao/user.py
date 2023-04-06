# Тут будут запросы к моделям sqlalchemy
from .daobase import DAOBase

class UserDAO(DAOBase):
  def __init__(self):
    super().__init__()
  
  async def read(self):
    from sqlalchemy import text
    # Select User
    user_stmt = text("select * from public.user")
    async with self.session as session, session.begin():
      result = await session.execute(user_stmt)
      usr = result.scalars()
      print(list(usr))
  
  async def create(self, data):
    pass

  async def delete(self, primarykey):
    pass

  async def update(self, primarykey, data):
    pass
from .daobase import DAOBase
from database import User
from sqlalchemy import select

# TODO: it seems not good to use this arch model->dao. where flexibliyu

class UserDAO(DAOBase):
  def __init__(self):
    super().__init__()
    self.user_model = User
 
  async def create(self, data: dict) -> None:
    async with self.session as session, session.begin():
      user = self.user_model(
        telegram_id=data["telegram_id"],
        first_name=data["first_name"],
        username=data["username"]
      )
      session.add(user)

  async def read(self, key: int):
    stmt = select(User).where(User.telegram_id == key)
    async with self.session as session, session.begin():
      result = await session.execute(stmt)
      result = result.first()
      return result


  async def update(self, primarykey, data):
    pass

  async def delete(self, primarykey):
    pass

    # from sqlalchemy import text
    # # Select User
    # user_stmt = text("select * from public.user")
    # async with self.session as session, session.begin():
    #   result = await session.execute(user_stmt)
    #   usr = result.scalars()
    #   print(list(usr))
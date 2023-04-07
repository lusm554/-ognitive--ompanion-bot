from .daobase import DAOBase
from database import User

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

  async def read(self):
    pass

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
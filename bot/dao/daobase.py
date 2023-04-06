from database import DB
from abc import ABC, abstractmethod

class DAOBase(ABC):
  """An abstract class that is used to interact with SQLAlchemy data models."""
  def __init__(self):
    self.session = DB.get_session() 

  @abstractmethod
  async def create(self, data):
    pass

  @abstractmethod
  async def read(self, primarykey):
    pass

  @abstractmethod
  async def update(self, primarykey, data):
    pass

  @abstractmethod
  async def delete(self, primarykey):
    pass
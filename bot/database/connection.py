from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from exceptions import DatabaseError

# TODO: as in `get_session` actual connection does not open, need to find where we can catch connection errors.

class PostgresConnection:
  def __init__(
    self,
    DIVERNAME: str,
    USERNAME: str,
    PASSWORD: str,
    HOST: str,
    DATABASE: str,
    DECLARATIVE_BASE: DeclarativeBase
  ):
    # Programmatic way to generate db url.
    self.__postgre_url__ = URL.create(
      drivername=DIVERNAME,
      username=USERNAME,
      password=PASSWORD,
      host=HOST,
      database=DATABASE
    )
    # Just engine, not actual connection. Connection opened only when using Session or connection. 
    self.engine = create_async_engine(
      self.__postgre_url__,
      echo=True
      )
    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    self.async_session_factory = async_sessionmaker(self.engine, expire_on_commit=False)
    self.Base = DECLARATIVE_BASE
    self.__connection_initiated__ = False

  async def init_db(self):
    """Create tables in database if not exists."""
    if self.__connection_initiated__:
      raise DeclarativeBase("Connection already initialized.")
    self.__connection_initiated__ = True
    async with self.engine.begin() as connection:
      await connection.run_sync(self.Base.metadata.create_all)
    return self
  
  def get_session(self) -> async_sessionmaker[AsyncSession]:
    """ Returns session object. Not connection."""
    session = self.async_session_factory()
    return session
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# TODO: as in `get_session` actual connection does not open, need to find where we can catch connection errors.

class DBConnection:
  """Singleton object of connection to database."""
  __instance__ = None
  __is_db_inited__ = False

  @staticmethod
  def __check_if_instance__(exist: bool = False, nexist: bool = False):
    """
    Decorator that check whether instance of this class exists or not.

    Parameters
    ----------
      exist : bool
        Flag for checking the existence of a class instance.
      nexist : bool
        Flag to check if the class instance does not exist
    """
    def decorator(func):
      def wrapper(*args, **kwargs):
        if exist and DBConnection.__instance__ is not None:
          raise Exception("Instance of DBConnection already exists.")
        if nexist and DBConnection.__instance__ is None:
          raise Exception("Instance of DBConnection doesn't exists.")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  @__check_if_instance__(exist=True)
  def __init__(
    self,
    DIVERNAME: str,
    USERNAME: str,
    PASSWORD: str,
    HOST: str,
    DATABASE: str,
    DECLARATIVE_BASE: DeclarativeBase
  ):
    DBConnection.__instance__ = self
    # Programmatic way to generate db url.
    self.__connection_url__ = URL.create(
      drivername=DIVERNAME,
      username=USERNAME,
      password=PASSWORD,
      host=HOST,
      database=DATABASE
    )
    # Just engine, not actual connection. Connection opened only when using Session or connection. 
    self.engine = create_async_engine(
      self.__connection_url__,
      echo=True
    )
    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    self.async_session_factory = async_sessionmaker(self.engine, expire_on_commit=False)
    self.Base = DECLARATIVE_BASE

  async def init_db(self):
    """Create tables in database if not exists."""
    if DBConnection.__is_db_inited__:
      raise Exception("Database already initialized.")
    DBConnection.__is_db_inited__ = True
    async with self.engine.begin() as connection:
      await connection.run_sync(self.Base.metadata.create_all)
    return self
  
  @staticmethod
  @__check_if_instance__(nexist=True)
  def get_instance():
    """Returns instance of this class."""
    return DBConnection.__instance__

  @staticmethod
  @__check_if_instance__(nexist=True)
  def get_session() -> async_sessionmaker[AsyncSession]:
    """Returns session object. Not connection."""
    session = DBConnection.__instance__.async_session_factory()
    return session
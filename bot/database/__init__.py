from config import PostgresDatabaseConfig
from .connection import DBConnection
from .data_model import Base 

# Getting DB object, not actual connection.
DB = DBConnection(
  DIVERNAME=PostgresDatabaseConfig.DRIVER,
  USERNAME=PostgresDatabaseConfig.USERNAME,
  PASSWORD=PostgresDatabaseConfig.PASSWORD,
  HOST=PostgresDatabaseConfig.HOST,
  DATABASE=PostgresDatabaseConfig.DBNAME,
  DECLARATIVE_BASE=Base
)
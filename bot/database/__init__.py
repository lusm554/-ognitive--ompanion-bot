from config import PostgresDatabaseConfig
from .connection import PostgresConnection
from .data_model import Base 

# получаем тут подключение
# инитиализируем базу данных тут
# отдаем подключение в маин

# Getting DB object, not actual connection.
DB = PostgresConnection(
  DIVERNAME=PostgresDatabaseConfig.DRIVER,
  USERNAME=PostgresDatabaseConfig.USERNAME,
  PASSWORD=PostgresDatabaseConfig.PASSWORD,
  HOST=PostgresDatabaseConfig.HOST,
  DATABASE=PostgresDatabaseConfig.DBNAME,
  DECLARATIVE_BASE=Base
)
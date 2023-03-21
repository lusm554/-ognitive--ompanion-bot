from config import PostgresDatabaseConfig
from .connection import PostgresDB

DB = PostgresDB(
  user=PostgresDatabaseConfig.USER,
  password=PostgresDatabaseConfig.PASSWORD,
  dbname=PostgresDatabaseConfig.DBNAME,
  host=PostgresDatabaseConfig.HOST,
  port=PostgresDatabaseConfig.PORT
)

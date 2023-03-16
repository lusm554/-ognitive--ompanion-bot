from config import SQLiteDatabaseConfig
import sqlite3
from . import setup_sqlite

class SQLite3:
  def __init__():
    setup_sqlite.setup()

  def get_db_connection():
    connection = sqlite3.connect(SQLiteDatabaseConfig.DB_FILE_NAME)
    cursor = connection.cursor()
    return cursor

class Postgres:
  pass

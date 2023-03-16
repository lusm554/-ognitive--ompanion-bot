from config import SQLiteDatabaseConfig
import sqlite3

def setup():
  connection = sqlite3.connect(SQLiteDatabaseConfig.DB_FILE_NAME)
  cursor = connection.cursor()
  cursor.execute(f"CREATE TABLE if not exist {SQLiteDatabaseConfig.TABLE_USERS} (name)")

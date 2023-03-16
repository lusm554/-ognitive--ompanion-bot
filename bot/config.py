"""
All dynamic bot settings are defined here.
"""

class DatabaseBase:
  TABLE_USERS = "users" 
  TABLE_TASKS = "tasks" 
  # in future
  #TABLE_BOARDS =
  #TABLE_LISTS =

class SQLiteDatabaseConfig(DatabaseBase):
  DB_FILE_NAME = "task-tracker.db"


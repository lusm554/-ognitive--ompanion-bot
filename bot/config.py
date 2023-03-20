from exceptions import MissingEnvironmentVariable
import dotenv
import os

dotenv.load_dotenv()

class DatabaseBase:
  DBNAME = "postgres"

class PostgresDatabaseConfig(DatabaseBase):
  try:
    USER = os.environ["USER"]
    PORT = os.environ["PORT"]
    HOST = os.environ["HOST"]
    PASSWORD = os.environ["PASSWORD"]
  except KeyError as keyname:
    raise MissingEnvironmentVariable(f"Variable {keyname} not found.")

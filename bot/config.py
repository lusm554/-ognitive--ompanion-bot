from exceptions import MissingEnvironmentVariable
import dotenv
import os

dotenv.load_dotenv()

class TelegramConfig:
  try:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
  except KeyError as keyname:
    raise MissingEnvironmentVariable(f"Variable {keyname} not found.")

class LoggingConfig:
  try:
    LOG_LEVEL = os.environ["LOG_LEVEL"]
  except KeyError as keyname:
    raise MissingEnvironmentVariable(f"Variable {keyname} not found.")

class DatabaseBase:
  DBNAME = "postgres"

class PostgresDatabaseConfig(DatabaseBase):
  try:
    DRIVER = "postgresql+asyncpg" # constant, this driver used for async sqlalchemy
    USERNAME = os.environ["POSTGRES_USER"]
    PORT = os.environ["POSTGRES_PORT"]
    HOST = os.environ["POSTGRES_HOST"]
    PASSWORD = os.environ["POSTGRES_PASSWORD"]
  except KeyError as keyname:
    raise MissingEnvironmentVariable(f"Variable {keyname} not found.")

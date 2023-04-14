import pytest, inspect, logging
from bot.config import TelegramConfig, LoggingConfig, DatabaseBase, PostgresDatabaseConfig

def test_telegram_config():
  config = TelegramConfig()
  assert inspect.isclass(TelegramConfig)
  assert "TELEGRAM_TOKEN" in (pair[0] for pair in inspect.getmembers(config))

def test_logging_config():
  config = LoggingConfig()
  assert inspect.isclass(LoggingConfig)
  assert "LOG_LEVEL" in (pair[0] for pair in inspect.getmembers(config))

def test_db_base():
  base = DatabaseBase()
  assert inspect.isclass(DatabaseBase)
  assert "DBNAME" in (pair[0] for pair in inspect.getmembers(base))

def test_postgres_config():
  config = PostgresDatabaseConfig()
  assert inspect.isclass(PostgresDatabaseConfig)
  assert "DRIVER" in (pair[0] for pair in inspect.getmembers(config))
  assert "USERNAME" in (pair[0] for pair in inspect.getmembers(config))
  assert "PORT" in (pair[0] for pair in inspect.getmembers(config))
  assert "HOST" in (pair[0] for pair in inspect.getmembers(config))
  assert "PASSWORD" in (pair[0] for pair in inspect.getmembers(config))


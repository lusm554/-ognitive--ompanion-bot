import logging
from config import LoggingConfig

def get_logger(name: str = None) -> logging.Logger:
  """ Generate logger by name. """
  logger = logging.getLogger(name)
  logger.setLevel(LoggingConfig.LOG_LEVEL)
  formatter = logging.Formatter(
      f"%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%m-%d-%Y %H:%M:%S %Z%z"
  )
  handler = logging.StreamHandler()
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger
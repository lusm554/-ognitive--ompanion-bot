class DatabaseError(Exception):
  """Describes error while interacting with DataBase."""
  pass

class MissingEnvironmentVariable(Exception):
  """Describes error of missing environment variable."""
  pass
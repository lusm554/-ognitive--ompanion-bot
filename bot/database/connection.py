import psycopg2 
from exceptions import DatabaseError

class PostgresDB:
  def __init__(self, user, password, dbname, host, port):
    self.password = password
    self.host = host
    self.port = port
    self.user = user
    self.dbname = dbname
    self._connection = None

  def get_connection(self) -> psycopg2.extensions.connection:
    try:
      connection = psycopg2.connect(
        password=self.password,
        host=self.host,
        port=self.port,
        user=self.user,
        dbname=self.dbname
      )
      self._connection = connection
      return connection
    except psycopg2.OperationalError as op_error:
      raise DatabaseError(f"An error occurred while connecting to the Postgres database.") from op_error
  
  def get_cursor(self) -> psycopg2.extensions.cursor:
    assert self._connection, "Connection not established"
    return self._connection.cursor()


from abc import ABC

class UserDAO(ABC):
  def __init__(self, db_connection):
    self.conn = db_connection
  
  def create_user(self, telegram_id, username, nickname, phone_number, created_at, updated_at):
    with self.conn.cursor() as cur:
      cur.execute("""
        INSERT INTO USERS (telegram_id, username, nickname, phone_number, created_at, updated_at) values
        (%s, %s, %s, %s, %s, %s)
      """, (telegram_id, username, nickname, phone_number, created_at, updated_at))
      self.conn.commit()
  
  def get_users(self):
    with self.conn.cursor() as cur:
      cur.execute("""
        select *
        from users
      """)
      return cur.fetchall()

class BoardDAO(ABC):
  ...

class BoardPermissionDAO(ABC):
  ...

class ListDAO(ABC):
  ...

class TaskDAO(ABC):
  ...

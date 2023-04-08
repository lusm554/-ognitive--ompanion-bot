from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List

# TODO: check for proper 'load strategy' for relationship in context of async operations.
# TODO: add created_at and updated_at

class Base(DeclarativeBase):
  """
  Base class used for declarative class definitions.
  The DeclarativeBase allows for the creation of new declarative bases in such a way that is compatible with type checkers.
  More on https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase 
  """
  pass

class User(Base):
  """
  The data model for the users table. The table contains all users who use this bot.
  The user is added on the first interaction.
  """
  __tablename__ = "user"
  id: Mapped[int] = mapped_column(primary_key=True)
  telegram_id: Mapped[str]
  username: Mapped[str]
  first_name: Mapped[str]
  # tasks: Mapped[List["Task"]] = relationship(back_populates="user", lazy="raise")
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, telegram_id={self.telegram_id!r}, username={self.username!r}, first_name={self.first_name!r})"

class Task(Base):
  """
  The data model for the tasks table. Each user can have tasks that are contained in this table.
  """
  __tablename__ = "task"
  id: Mapped[int] = mapped_column(primary_key=True)
  telegram_user_id: Mapped[str]
  name: Mapped[str]
  status: Mapped[str]
  # user: Mapped[User] = relationship(back_populates="tasks", lazy="raise")
  def __repr__(self) -> str:
    return f"Task(id={self.id!r}, user_id={self.user_id!r}, task_number={self.task_number!r}, description={self.description!r}, status={self.status!r})"
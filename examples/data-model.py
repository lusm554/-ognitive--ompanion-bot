from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session

# Just engine, not actual connection. Connection opened only when using Session or connection. 
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# for MetaData object
class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "user"
  id: Mapped[int] = mapped_column(primary_key=True)
  telegram_id: Mapped[int]
  nickname: Mapped[str]
  fullname: Mapped[str]
  tasks: Mapped[List["Task"]] = relationship(back_populates="user")
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, telegram_id={self.telegram_id!r}, nickname={self.nickname!r}, fullname={self.fullname!r})"

class Task(Base):
  __tablename__ = "task"
  id: Mapped[int] = mapped_column(primary_key=True)
  user_id = mapped_column(ForeignKey("user.id"))
  task_number: Mapped[int]
  name: Mapped[str]
  description: Mapped[str]
  status: Mapped[str]
  user: Mapped[User] = relationship(back_populates="tasks")
  def __repr__(self) -> str:
    return f"Task(id={self.id!r}, user_id={self.user_id!r}, task_number={self.task_number!r}, description={self.description!r}, status={self.status!r})"


# Create if exists all tables in Base
Base.metadata.create_all(engine)


# Insert User
with Session(engine) as session:
  user = User(
    telegram_id=1,
    nickname="lusm",
    fullname="Nikita"
  )
  task = Task(
    #user_id=1,
    task_number=1,
    name="Math",
    description="math",
    status="done"
  )
  session.add(user)
  session.add(task)
  session.commit()

# Select User
user_stmt = select(User).where(User.nickname=="lusm")
task_stmt = select(Task).where(Task.name=="Math")
with Session(engine) as session:
  for row in session.execute(user_stmt):
    print(row)
  for row in session.execute(task_stmt):
    print(row)


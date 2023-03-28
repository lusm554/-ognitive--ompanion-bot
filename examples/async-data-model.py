import asyncio

#from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import URL # for gen db url programmatically 
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select

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


async def insert_user(async_session: async_sessionmaker[AsyncSession]):
	user = User(
		telegram_id=1,
		nickname="lusm",
		fullname="Nikita"
	)
	task = Task(
		task_number=1,
		name="Math",
		description="math",
		status="done"
	)
	# Insert User
	async with async_session() as session, session.begin():
		session.add(user)
		session.add(task)

async def select_user(async_session: async_sessionmaker[AsyncSession]):
	# Select User
	user_stmt = select(User).where(User.nickname=="lusm")
	task_stmt = select(Task).where(Task.name=="Math")
	async with async_session() as session, session.begin():
		result = await session.execute(user_stmt)
		usr = result.scalars()
		for u in usr:
			print(u)
		result = await session.execute(task_stmt)
		tsk = result.scalars()
		for t in tsk:
			print(t)

def get_url():
	url_object = URL.create(
		drivername="postgresql+asyncpg",
		username="postgres",
		password="mysecretpassword",
		host="127.0.0.1",
		database="postgres"
	)
	return url_object

async def main():
	# Just engine, not actual connection. Connection opened only when using Session or connection. 
	engine = create_async_engine(get_url(), echo=True)

	# async_sessionmaker: a factory for new AsyncSession objects.
	# expire_on_commit - don't expire objects after transaction commit
	async_session = async_sessionmaker(engine, expire_on_commit=False)

	# Create if not exists all tables in Base
	async with engine.begin() as connection:
		await connection.run_sync(Base.metadata.create_all)
	await insert_user(async_session)	
	await select_user(async_session)

	# for AsyncEngine created in function scope, close and
	# clean-up pooled connections
	await engine.dispose()

asyncio.run(main())

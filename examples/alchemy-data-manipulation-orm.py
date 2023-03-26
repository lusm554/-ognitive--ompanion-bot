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

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# for MetaData object
class Base(DeclarativeBase):
  pass

# If work with ORM
# Declarative Mapping 
class User(Base):
  __tablename__ = "user_account"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30))
  fullname: Mapped[Optional[str]]
  addresses: Mapped[List["Address"]] = relationship(back_populates="user")
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# If work with ORM
# Declarative Mapping 
class Address(Base):
  __tablename__ = "address"
  id: Mapped[int] = mapped_column(primary_key=True)
  email_address: Mapped[str]
  user_id = mapped_column(ForeignKey("user_account.id"))
  user: Mapped[User] = relationship(back_populates="addresses")
  def __repr__(self) -> str:
    return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# for ORM example
Base.metadata.create_all(engine)


# If work with ORM
# Simple select
stmt = select(User).where(User.name == "Sola")
with Session(engine) as session:
  for row in session.execute(stmt):
    print(row)


squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
with Session(engine) as session:
	session.add(squidward)
	session.add(krabs)
	session.commit()

from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# If work directly to Core
metadata_obj = MetaData()

# If work directly to Core
user_table = Table(
  "user_account",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("name", String(30)),
  Column("fullname", String),
)

# If work directly to Core
address_table = Table(
  "address",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("user_id", ForeignKey("user_account.id"), nullable=False),
  Column("email_address", String, nullable=False),
)

# for Core example
metadata_obj.create_all(engine)


from sqlalchemy.orm import DeclarativeBase

# for MetaData object
class Base(DeclarativeBase):
  pass

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

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

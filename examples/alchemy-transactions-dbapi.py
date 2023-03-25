from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# If work directly with Core
# Open connection without commit
with engine.connect() as conn:
  result = conn.execute(text("select 'hello world'"))
  print(result.all())
  # will be ROLLBACK, because we don't commit connection


# If work directly with Core
# Open connection with commit
with engine.connect() as conn:
  conn.execute(text("create table supercooldata (x int, y int)"))
  conn.execute(
    text("insert into supercooldata values (:x, :y)"),
    [{"x": 1, "y": 1}, {"x": 2, "y": 5}, {"x": 7, "y": 7}, {"x": 3, "y": 2}]
  )
  conn.commit()


# If work directly with Core
# Open connection with commit through begin
#with engine.begin() as conn:
#  conn.execute(text("create table supercooldata (x int, y int)"))
#  conn.execute(
#    text("insert into supercooldata values (:x, :y)"),
#    [{"x": 1, "y": 1}, {"x": 2, "y": 5}]
#  )

# If work with Core or ORM
# Select rows through attr name
with engine.connect() as conn:
  result = conn.execute(text("select x, y from supercooldata"))
  for row in result:
    print(f"x: {row.x} y: {row.y}")

# If work with Core or ORM
# Sending parameters
with engine.connect() as conn:
  result = conn.execute(text("select x, y from supercooldata where y > :y"), {"y": 5})
  for row in result:
    print(f"x: {row.x} y: {row.y}")

# If work with ORM
# Within ORM Session object is like Connection object
stmt = text("select x, y from supercooldata where y > :y")
with Session(engine) as session:
  result = session.execute(stmt, {"y": 5})
  for row in result:
    print(f"x: {row.x} y: {row.y}")


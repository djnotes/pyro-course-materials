from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Double, String, create_engine
import os

class Base(DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key = True)
    author_id: Mapped[float] = mapped_column(Double())
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(1024))

username = os.environ.get('MARIADB_USER')
password = os.environ.get('MARIADB_PASSWORD')
host = os.environ.get('MARIADB_HOST')
dbname = os.environ.get('MARIADB_DATABASE')

engine = create_engine(f"mysql://{username}:{password}@{host}:3306/{dbname}")

Base.metadata.create_all(engine)

def get_db():
    """
    Gets us a connection to database
    """
    return Session(engine)





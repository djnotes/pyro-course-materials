from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import dill

import os


class Base(DeclarativeBase):
    pass

class UserSession(Base):
    __tablename__ = "user_session"
    
    name: Mapped[str] = mapped_column(String(256), primary_key=True)
    value: Mapped[str] = mapped_column(String(1024))

username = os.environ.get('MARIADB_USER')
password = os.environ.get('MARIADB_PASSWORD')
host = os.environ.get('MARIADB_HOST')
db = os.environ.get('MARIADB_DATABASE')

engine = create_engine(f"sqlite:///app-data.db")

Base.metadata.create_all(engine)

class Db:
    def __init__(self):
        self.db = Session(engine)
    def _get_user_session(self, uid, key):
        stmt = select(UserSession).where(UserSession.name == str(uid) + "." + key)
        return self.db.scalars(stmt).one_or_none()

    def update_user_session(self, uid, key, value):
        s = self._get_user_session(uid, key)
        if s:
            s.value = dill.dumps(value)
        else:
            s = UserSession(name = str(uid) + "." + key, value = dill.dumps(value))
            self.db.add(s)
        self.db.commit()

    def get_session_item(self, uid, key):
        s = self._get_user_session(uid, key)
        return dill.loads(s.value) if s else None
    def clear_session(self, uid):
        stmt = select(UserSession).where(UserSession.name.startswith(str(uid)))
        ss = self.db.scalars(stmt).all()
        for s in ss:
            self.db.delete(s)
        
        self.db.commit()
    

    
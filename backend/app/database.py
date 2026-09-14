from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(connection, _):
    if settings.database_url.startswith("sqlite"):
        cursor = connection.cursor(); cursor.execute("PRAGMA foreign_keys=ON"); cursor.close()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
class Base(DeclarativeBase): pass
def get_db():
    with SessionLocal() as db:
        try:
            yield db; db.commit()
        except Exception:
            db.rollback(); raise
@contextmanager
def transaction():
    with SessionLocal.begin() as db: yield db

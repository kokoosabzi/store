from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


connect_args = (
    {"check_same_thread": False, "timeout": 30}
    if settings.database_url.startswith("sqlite")
    else {}
)
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)


@event.listens_for(engine, "connect")
def enable_sqlite_pragmas(connection, _):
    if settings.database_url.startswith("sqlite"):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=30000")
        if not settings.database_url.endswith(":memory:"):
            cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
        if not db.info.get("skip_commit"):
            db.commit()
    except Exception:
        if not db.info.get("skip_commit"):
            db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def transaction():
    with SessionLocal.begin() as db:
        yield db

"""SQLite-safe local backup and offline restore helpers."""
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import tempfile
from contextlib import closing

from sqlalchemy.engine import make_url

from .config import settings


def database_path() -> Path:
    url = make_url(settings.database_url)
    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise ValueError("پشتیبان‌گیری فقط برای دیتابیس SQLite فایل‌محور پشتیبانی می‌شود.")
    path = Path(url.database).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def validate_backup(path: Path) -> dict:
    if not path.is_file():
        raise ValueError("فایل پشتیبان وجود ندارد.")
    try:
        with closing(sqlite3.connect(str(path), timeout=30)) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            version = (
                connection.execute("SELECT version_num FROM alembic_version LIMIT 1").fetchone()
                if "alembic_version" in tables
                else None
            )
    except sqlite3.DatabaseError as error:
        raise ValueError("فایل پشتیبان SQLite معتبر نیست.") from error

    required = {"alembic_version", "products", "sales", "purchases"}
    if not integrity or integrity[0] != "ok" or not required.issubset(tables) or not version:
        raise ValueError("پشتیبان سالم نیست یا ساختار مورد انتظار فروشگاه را ندارد.")
    return {
        "path": str(path),
        "integrity": integrity[0],
        "tables": len(tables),
        "schema_version": version[0],
    }


def _sqlite_snapshot(source_path: Path, target_path: Path) -> None:
    with closing(sqlite3.connect(str(source_path), timeout=30)) as source:
        with closing(sqlite3.connect(str(target_path), timeout=30)) as destination:
            source.backup(destination)
            destination.commit()
            mode = destination.execute("PRAGMA journal_mode=DELETE").fetchone()
            if not mode or mode[0].lower() != "delete":
                raise ValueError("ساخت فایل پشتیبان مستقل SQLite ناموفق بود.")
            destination.commit()


def _temporary_path(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=".lcc-", suffix=".tmp", dir=directory)
    os.close(descriptor)
    return Path(name)


def create_backup() -> dict:
    source_path = database_path()
    if not source_path.is_file():
        raise ValueError("پایگاه‌داده برای پشتیبان‌گیری هنوز ایجاد نشده است.")
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = settings.backup_dir / f"local-commerce-{timestamp}.db"
    temporary = _temporary_path(settings.backup_dir)
    try:
        _sqlite_snapshot(source_path, temporary)
        validation = validate_backup(temporary)
        os.replace(temporary, target)
        validation["path"] = str(target)
        return validation
    finally:
        temporary.unlink(missing_ok=True)


def restore_backup(backup_name: str) -> dict:
    """Restore a validated backup after the caller closes DB sessions and disposes the engine."""
    backup_root = settings.backup_dir.resolve()
    candidate = (backup_root / backup_name).resolve()
    if candidate.parent != backup_root or candidate.suffix.lower() != ".db":
        raise ValueError("نام فایل پشتیبان معتبر نیست.")
    validation = validate_backup(candidate)

    source_path = database_path()
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    current_backup = create_backup() if source_path.is_file() else None
    temporary = _temporary_path(source_path.parent)
    try:
        _sqlite_snapshot(candidate, temporary)
        validate_backup(temporary)

        # The request session and engine must be closed/disposed by the API
        # before this point. Remove old WAL sidecars only after the current
        # state has been backed up and the restore snapshot has been validated.
        Path(f"{source_path}-wal").unlink(missing_ok=True)
        Path(f"{source_path}-shm").unlink(missing_ok=True)
        os.replace(temporary, source_path)
        restored = validate_backup(source_path)
        return {
            "restored": validation["path"],
            "schema_version": restored["schema_version"],
            "pre_restore_backup": current_backup["path"] if current_backup else None,
        }
    finally:
        temporary.unlink(missing_ok=True)

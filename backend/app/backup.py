"""SQLite-safe local backup and verification helpers."""
from datetime import datetime
from pathlib import Path
import sqlite3
from .config import settings


def database_path() -> Path:
    prefix = 'sqlite:///./'
    if not settings.database_url.startswith(prefix):
        raise ValueError('پشتیبان‌گیری فقط برای مسیر SQLite محلی پشتیبانی می‌شود.')
    return Path(settings.database_url.removeprefix(prefix)).resolve()


def validate_backup(path: Path) -> dict:
    if not path.is_file():
        raise ValueError('فایل پشتیبان وجود ندارد.')
    with sqlite3.connect(path) as connection:
        integrity = connection.execute('PRAGMA integrity_check').fetchone()[0]
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if integrity != 'ok' or not {'products', 'sales', 'purchases'}.issubset(tables):
        raise ValueError('پشتیبان سالم یا کامل نیست.')
    return {'path': str(path), 'integrity': integrity, 'tables': len(tables)}


def create_backup() -> dict:
    source_path = database_path()
    if not source_path.is_file():
        raise ValueError('پایگاه‌داده برای پشتیبان‌گیری هنوز ایجاد نشده است.')
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    target = settings.backup_dir / f"local-commerce-{datetime.now():%Y%m%d-%H%M%S}.db"
    with sqlite3.connect(source_path) as source, sqlite3.connect(target) as destination:
        source.backup(destination)
    return validate_backup(target)


def restore_backup(backup_name: str) -> dict:
    """Validate a named local backup, safeguard current data, then atomically replace it."""
    candidate = (settings.backup_dir / backup_name).resolve()
    backup_root = settings.backup_dir.resolve()
    if candidate.parent != backup_root or candidate.suffix != '.db':
        raise ValueError('نام فایل پشتیبان معتبر نیست.')
    validation = validate_backup(candidate)
    current_backup = create_backup()
    source_path = database_path()
    temporary = source_path.with_suffix('.restore.tmp')
    import shutil
    shutil.copy2(candidate, temporary)
    temporary.replace(source_path)
    return {'restored': validation['path'], 'pre_restore_backup': current_backup['path']}

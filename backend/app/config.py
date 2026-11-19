from pathlib import Path
import os

from sqlalchemy.engine import URL, make_url


DEFAULT_DATABASE_URL = "sqlite:///./data/local_commerce.db"


def database_url_for_data_directory(directory: str | Path) -> str:
    data_directory = Path(directory).expanduser().resolve()
    data_directory.mkdir(parents=True, exist_ok=True)
    return URL.create(
        "sqlite",
        database=str(data_directory / "local_commerce.db"),
    ).render_as_string(hide_password=False)


class Settings:
    app_name = "Local Commerce Core"
    data_directory = Path(
        os.getenv("LCC_DATA_DIR", "./data")
    ).expanduser().resolve()
    database_url = (
        os.getenv("LCC_DATABASE_URL")
        or (
            database_url_for_data_directory(data_directory)
            if os.getenv("LCC_DATA_DIR")
            else DEFAULT_DATABASE_URL
        )
    )
    allow_negative_stock = os.getenv(
        "LCC_ALLOW_NEGATIVE_STOCK", "false"
    ).lower() == "true"
    backup_dir = Path(
        os.getenv(
            "LCC_BACKUP_DIR",
            str(data_directory.parent / "backups")
            if os.getenv("LCC_DATA_DIR")
            else "./backups",
        )
    ).expanduser().resolve()
    run_dir = Path(
        os.getenv(
            "LCC_RUN_DIR",
            str(data_directory.parent / "run")
            if os.getenv("LCC_DATA_DIR")
            else "./run",
        )
    ).expanduser().resolve()
    log_dir = Path(
        os.getenv(
            "LCC_LOG_DIR",
            str(data_directory.parent / "logs")
            if os.getenv("LCC_DATA_DIR")
            else "./logs",
        )
    ).expanduser().resolve()


settings = Settings()

_database_url = make_url(settings.database_url)
if _database_url.get_backend_name() == "sqlite" and _database_url.database not in (None, ":memory:"):
    database_file = Path(_database_url.database).expanduser()
    if not database_file.is_absolute():
        database_file = Path.cwd() / database_file
    database_file.parent.mkdir(parents=True, exist_ok=True)

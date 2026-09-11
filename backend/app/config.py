from pathlib import Path
import os
class Settings:
    app_name = "Local Commerce Core"
    database_url = os.getenv("LCC_DATABASE_URL", "sqlite:///./data/local_commerce.db")
    allow_negative_stock = os.getenv("LCC_ALLOW_NEGATIVE_STOCK", "false").lower() == "true"
    backup_dir = Path(os.getenv("LCC_BACKUP_DIR", "./backups"))
settings = Settings()
if settings.database_url.startswith('sqlite:///./'):
    Path(settings.database_url.removeprefix('sqlite:///./')).parent.mkdir(parents=True, exist_ok=True)

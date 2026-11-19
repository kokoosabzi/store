from pathlib import Path

from sqlalchemy.engine import make_url

from backend.app.config import database_url_for_data_directory


def test_windows_data_directory_url_is_absolute_and_creates_folder(tmp_path):
    data_directory = tmp_path / "Local Commerce Core user data"
    url = make_url(database_url_for_data_directory(data_directory))

    assert url.get_backend_name() == "sqlite"
    assert Path(url.database).resolve() == (data_directory / "local_commerce.db").resolve()
    assert data_directory.is_dir()

import os
import sqlite3
from pathlib import Path

import pytest

os.environ['LCC_DATABASE_URL'] = 'sqlite:///./test_local_commerce.db'
from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.app.config import settings
from backend.app.database import Base, engine
from backend.app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "backup_dir", tmp_path / "backups")
    engine.dispose()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with engine.begin() as connection:
        connection.exec_driver_sql("DROP TABLE IF EXISTS alembic_version")
        connection.exec_driver_sql(
            "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
        )
        connection.exec_driver_sql(
            "INSERT INTO alembic_version(version_num) VALUES ('0004_notifications')"
        )
    with TestClient(app) as test_client:
        yield test_client
    engine.dispose()


def _setup_pin(client):
    response = client.post("/api/security/setup-pin", json={"pin": "1234"})
    assert response.status_code == 201


def _create_product(client, name):
    response = client.post("/api/products", json={"name": name, "retail_price": "120"})
    assert response.status_code == 201
    return response.json()


def test_api_backup_and_restore_closes_database_session_and_preserves_current_state(client):
    _setup_pin(client)
    original = _create_product(client, "کالای قبل از پشتیبان")

    backup_response = client.post("/api/backups")
    assert backup_response.status_code == 201
    backup_name = Path(backup_response.json()["path"]).name
    assert (settings.backup_dir / backup_name).is_file()

    _create_product(client, "کالای بعد از پشتیبان")
    assert len(client.get("/api/products").json()) == 2

    restored = client.post(
        "/api/restore",
        json={"backup_name": backup_name, "pin": "1234"},
    )
    assert restored.status_code == 200
    assert restored.json()["schema_version"] == "0004_notifications"
    assert Path(restored.json()["pre_restore_backup"]).is_file()

    products = client.get("/api/products")
    assert products.status_code == 200
    assert [item["id"] for item in products.json()] == [original["id"]]
    assert products.json()[0]["name"] == "کالای قبل از پشتیبان"


def test_restore_requires_correct_manager_pin_and_keeps_current_database(client):
    _setup_pin(client)
    original = _create_product(client, "کالای محافظت‌شده")
    backup_response = client.post("/api/backups")
    backup_name = Path(backup_response.json()["path"]).name
    _create_product(client, "کالای جدید")

    denied = client.post(
        "/api/restore",
        json={"backup_name": backup_name, "pin": "0000"},
    )
    assert denied.status_code == 403
    assert len(client.get("/api/products").json()) == 2
    assert original["name"] == "کالای محافظت‌شده"


def test_restore_rejects_corrupt_or_path_traversal_backup_without_changing_data(client):
    _setup_pin(client)
    product = _create_product(client, "کالای سالم")
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    corrupt = settings.backup_dir / "corrupt.db"
    corrupt.write_bytes(b"not a sqlite database")

    invalid = client.post(
        "/api/restore",
        json={"backup_name": corrupt.name, "pin": "1234"},
    )
    assert invalid.status_code == 422

    traversal = client.post(
        "/api/restore",
        json={"backup_name": "../test_local_commerce.db", "pin": "1234"},
    )
    assert traversal.status_code == 422
    assert [item["id"] for item in client.get("/api/products").json()] == [product["id"]]

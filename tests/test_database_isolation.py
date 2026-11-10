import pytest

from app import create_app, db
from config import Config


def test_client_uses_an_in_memory_engine(client):
    with client.application.app_context():
        assert set(db.engines) == {None}
        assert db.engine.url.get_backend_name() == "sqlite"
        assert db.engine.url.database == ":memory:"


def test_override_prevents_access_to_configured_database(monkeypatch, tmp_path):
    sentinel_db = tmp_path / "must-not-be-created.sqlite"
    monkeypatch.setattr(Config, "SQLALCHEMY_DATABASE_URI", f"sqlite:///{sentinel_db}")

    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-key-unique-not-for-production-2026",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_BINDS": {},
    })
    with app.app_context():
        assert db.engine.url.get_backend_name() == "sqlite"
        assert db.engine.url.database == ":memory:"
        db.create_all()
        assert not sentinel_db.exists()
        db.session.remove()
        db.engine.dispose()


def test_render_without_database_url_fails_before_initialization(monkeypatch):
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL is required"):
        create_app({"SECRET_KEY": "test-only-key-unique-not-for-production-2026"})

import sqlite3

from sqlalchemy import create_engine, text

import migrate_data


def test_migration_inserts_source_rows(monkeypatch, tmp_path):
    tables = ["users", "categories", "recipes", "meal_plans", "meal_entries", "favorites"]
    source = tmp_path / "source.sqlite"
    with sqlite3.connect(source) as connection:
        for table in tables:
            connection.execute(f"CREATE TABLE {table} (id INTEGER, ativo INTEGER)")
        connection.execute("INSERT INTO users (id, ativo) VALUES (1, 1)")

    target = create_engine("sqlite:///:memory:")
    with target.begin() as connection:
        for table in tables:
            connection.execute(text(f"CREATE TABLE {table} (id INTEGER, ativo INTEGER)"))

    monkeypatch.setattr(migrate_data, "SQLITE_DB", str(source))
    monkeypatch.setattr(migrate_data, "create_engine", lambda _url: target)
    monkeypatch.setenv("DATABASE_URL", "unused-test-value")
    migrate_data.migrate()

    with target.connect() as connection:
        assert connection.execute(text("SELECT id, ativo FROM users")).all() == [(1, 1)]
    target.dispose()

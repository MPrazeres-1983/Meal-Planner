import os
os.environ.setdefault("SECRET_KEY", "test-only-key-unique-not-for-production-2026")

import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-key-unique-not-for-production-2026",
        "WTF_CSRF_SECRET_KEY": "test-only-csrf-unique-not-for-production-2026",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_BINDS": {},
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        # Verify the initialized engines, not merely the configuration string.
        if (set(db.engines) != {None}
                or db.engine.url.get_backend_name() != "sqlite"
                or db.engine.url.database != ":memory:"):
            raise RuntimeError("Test database must be an isolated in-memory SQLite database")
        db.create_all()
        try:
            yield app.test_client()
        finally:
            db.session.remove()
            db.engine.dispose()

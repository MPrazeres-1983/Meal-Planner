import os
os.environ.setdefault("SECRET_KEY", "test-only-key-unique-not-for-production-2026")

import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    assert (
        "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]
    ), "NUNCA correr testes na base de dados de produção!"

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()  # O client é o cliente de teste do Flask

        # Opcional: limpar BD no fim (para SQLite em memória não é obrigatório)
        db.session.remove()
        db.drop_all()

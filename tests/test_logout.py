"""
test_logout.py

Testa se o logout limpa a sessão e redireciona corretamente.
"""

import re

import pytest
from app.models.user import User
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador(client):
    """
    Cria utilizador válido na base de dados de teste antes de cada teste.
    """
    with client.application.app_context():

        utilizador = User(
            nome="Utilizador Teste",
            email="teste@email.com",
            nivel=1,
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()


def test_logout(client):
    """
    Testa se o logout limpa a sessão e redireciona corretamente.
    """
    # Fazer login
    client.post(
        "/auth/login",
        data={"email": "teste@email.com", "password": "senha123"},
        follow_redirects=True,
    )

    # Fazer logout
    response = client.post("/auth/logout", follow_redirects=True)

    assert response.status_code == 200
    assert "Sessão terminada" in response.get_data(as_text=True)


def test_logout_requires_post_and_csrf(client):
    with client.application.app_context():
        user_id = User.query.filter_by(email="teste@email.com").one().id
    with client.session_transaction() as session:
        session["user_id"] = user_id

    client.application.config["WTF_CSRF_ENABLED"] = True
    assert client.get("/auth/logout").status_code == 405
    assert client.post("/auth/logout").status_code == 400
    with client.session_transaction() as session:
        assert session["user_id"] == user_id

    page = client.get("/home").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    assert client.post("/auth/logout", data={"csrf_token": token}).status_code == 302
    with client.session_transaction() as session:
        assert "user_id" not in session

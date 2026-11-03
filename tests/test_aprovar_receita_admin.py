"""
test_aprovar_receita_admin.py

Testa se um administrador consegue aprovar uma receita pendente.
"""

import pytest
from app.models.user import User
from app.models.recipe import Recipe
from app.models.category import Category
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Prepara admin, categoria e receita pendente antes de cada teste.
    """
    with client.application.app_context():
        # Criar admin
        admin = User(nome="Admin", email="admin@email.com", nivel=3)
        admin.set_password("admin123")
        db.session.add(admin)

        # Criar categoria
        categoria = Category(nome="Massas")
        db.session.add(categoria)
        db.session.commit()

        # Criar receita pendente
        receita = Recipe(
            titulo="Lasanha",
            descricao="Camadas de massa e carne",
            ingredientes="massa, carne, queijo",
            instrucoes="1. Montar\n2. Forno",
            tempo_preparacao=45,
            dificuldade=2,
            tags="massa",
            categoria_id=categoria.id,
            publicada=False,
            aprovada=False,
            fonte="utilizador",
            utilizador_id=admin.id,
        )
        db.session.add(receita)
        db.session.commit()

        # Login admin
        client.post(
            "/auth/login",
            data={"email": "admin@email.com", "password": "admin123"},
            follow_redirects=True,
        )


def test_aprovar_receita(client):
    """
    Aprova a receita 1 e verifica se a alteração foi efetuada.
    """
    response = client.post("/admin/aprovar_receita/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Receita aprovada com sucesso" in response.get_data(as_text=True)

    # Verificar se a receita está mesmo aprovada
    with client.application.app_context():
        receita = db.session.get(Recipe, 1)
        assert receita.aprovada is True

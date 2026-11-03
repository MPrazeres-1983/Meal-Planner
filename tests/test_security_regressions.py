"""Security regression tests for ownership and administrator routes."""
from datetime import date
from app import db
from app.models.user import User
from app.models.meal_plan import MealPlan


def test_other_user_cannot_delete_plan(client):
    with client.application.app_context():
        a = User(nome="A", email="owner@local.test", nivel=1)
        a.set_password("owner-password")
        b = User(nome="B", email="other@local.test", nivel=1)
        b.set_password("other-password")
        db.session.add_all([a, b]); db.session.commit()
        plan = MealPlan(utilizador_id=a.id, data_inicio=date.today())
        db.session.add(plan); db.session.commit()
        plan_id = plan.id
    client.post("/auth/login", data={"email": "other@local.test", "password": "other-password"})
    response = client.post(f"/planos/apagar/{plan_id}", follow_redirects=False)
    assert response.status_code == 302
    with client.application.app_context():
        assert db.session.get(MealPlan, plan_id) is not None


def test_admin_detail_and_edit_blocked_for_non_admin(client):
    with client.application.app_context():
        user = User(nome="Normal", email="normal@local.test", nivel=1)
        user.set_password("test-password")
        db.session.add(user); db.session.commit()
        user_id = user.id
    client.post("/auth/login", data={"email": "normal@local.test", "password": "test-password"})
    for path in [f"/admin/utilizador/{user_id}", f"/admin/utilizador/{user_id}/editar"]:
        response = client.get(path, follow_redirects=False)
        assert response.status_code == 302
        assert "/admin/" not in response.headers["Location"]


def test_approval_is_not_allowed_via_get(client):
    assert client.get("/admin/aprovar_receita/1").status_code == 405
    assert client.get("/admin/recusar_receita/1").status_code == 405

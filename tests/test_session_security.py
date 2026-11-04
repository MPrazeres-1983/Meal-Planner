"""Regression tests for session revocation and CSRF after the security fixes."""
from datetime import date

from app.db import db
from app.models.user import User
from app.models.meal_plan import MealPlan


def _user(email, nivel=1, ativo=True):
    u = User(nome="QA Test", email=email, nivel=nivel, ativo=ativo)
    u.set_password("test-only-password")
    db.session.add(u)
    db.session.commit()
    return u


def test_blocked_user_loses_existing_session(client):
    with client.application.app_context():
        user_id = _user("blocked@local.test", ativo=False).id

    with client.session_transaction() as session:
        session["user_id"] = user_id
        session["user_nivel"] = 3

    response = client.get("/home")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_deleted_user_loses_existing_session(client):
    with client.session_transaction() as session:
        session["user_id"] = 999999
        session["user_nivel"] = 3
    response = client.get("/home")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_demoted_after_login_loses_privileges(client):
    with client.application.app_context():
        user_id = _user("demoted@local.test", nivel=1).id

    # Simulate a previously valid administrator cookie after DB demotion.
    with client.session_transaction() as session:
        session["user_id"] = user_id
        session["user_nivel"] = 3

    response = client.get(f"/admin/utilizador/{user_id}")
    assert response.status_code == 302
    assert "/home" in response.headers["Location"]
    with client.session_transaction() as session:
        assert session["user_nivel"] == 1


def test_delete_plan_requires_csrf_when_enabled(client):
    with client.application.app_context():
        user_id = _user("owner-csrf@local.test").id
        plan = MealPlan(utilizador_id=user_id, data_inicio=date.today())
        db.session.add(plan)
        db.session.commit()
        plan_id = plan.id

    with client.session_transaction() as session:
        session["user_id"] = user_id
        session["user_nivel"] = 1

    client.application.config["WTF_CSRF_ENABLED"] = True
    response = client.post(f"/planos/apagar/{plan_id}")
    assert response.status_code == 400
    with client.application.app_context():
        assert db.session.get(MealPlan, plan_id) is not None


def test_delete_other_users_plan_is_rejected_even_with_valid_session(client):
    with client.application.app_context():
        owner_id = _user("owner-idor@local.test").id
        other_id = _user("other-idor@local.test").id
        plan = MealPlan(utilizador_id=owner_id, data_inicio=date.today())
        db.session.add(plan)
        db.session.commit()
        plan_id = plan.id

    with client.session_transaction() as session:
        session["user_id"] = other_id
        session["user_nivel"] = 1

    response = client.post(f"/planos/apagar/{plan_id}")
    assert response.status_code == 302
    with client.application.app_context():
        assert db.session.get(MealPlan, plan_id) is not None

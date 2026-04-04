from fastapi.testclient import TestClient

from app.main import app
from app.core.security import create_token


client = TestClient(app)


def auth_header(role: str = "customer"):
    token = create_token({"user_id": "user-1", "role": role})
    return {"Authorization": f"Bearer {token}"}


def test_register_accepts_role_property(monkeypatch):
    def fake_register(user):
        assert user.mobile_number == "9999999999"
        assert user.password == "secret123"
        assert user.role == "admin"
        return {"message": "User registered successfully", "user_id": "abc123"}

    monkeypatch.setattr("app.controllers.auth_controller.register", fake_register)

    response = client.post(
        "/auth/register",
        json={"mobile_number": "9999999999", "password": "secret123", "role": "admin"},
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == "abc123"


def test_login_accepts_mobile_and_password(monkeypatch):
    def fake_login(user):
        assert user.mobile_number == "9999999999"
        assert user.password == "secret123"
        return {"access_token": create_token({"user_id": "user-1", "role": "admin"}), "token_type": "bearer"}

    monkeypatch.setattr("app.controllers.auth_controller.login", fake_login)

    response = client.post(
        "/auth/login",
        json={"mobile_number": "9999999999", "password": "secret123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_plan_create_requires_admin_and_accepts_required_properties(monkeypatch):
    def fake_create_plan_service(plan):
        assert plan.name == "Premium"
        assert plan.price == 499
        assert plan.validity_days == 30
        assert plan.included_apps == ["Netflix", "Prime"]
        return {"message": "Plan created successfully", "plan_id": "plan123"}

    monkeypatch.setattr("app.controllers.plan_controller.create_plan_service", fake_create_plan_service)

    payload = {
        "name": "Premium",
        "price": 499,
        "validity_days": 30,
        "included_apps": ["Netflix", "Prime"],
    }

    forbidden = client.post("/plans/", json=payload, headers=auth_header("customer"))
    assert forbidden.status_code == 403

    ok = client.post("/plans/", json=payload, headers=auth_header("admin"))
    assert ok.status_code == 200
    assert ok.json()["plan_id"] == "plan123"


def test_content_create_requires_admin_and_accepts_required_properties(monkeypatch):
    def fake_add_content(content):
        assert content.title == "Movie 1"
        assert content.platform == "Netflix"
        assert content.category == "Movies"
        return {"message": "Content added successfully", "content_id": "content123"}

    monkeypatch.setattr("app.controllers.content_controller.add_content", fake_add_content)

    payload = {"title": "Movie 1", "platform": "Netflix", "category": "Movies"}

    forbidden = client.post("/content/", json=payload, headers=auth_header("customer"))
    assert forbidden.status_code == 403

    ok = client.post("/content/", json=payload, headers=auth_header("admin"))
    assert ok.status_code == 200
    assert ok.json()["content_id"] == "content123"


def test_subscribe_accepts_plan_id_property(monkeypatch):
    def fake_subscribe(user_id, plan_id):
        assert user_id == "user-1"
        assert plan_id == "507f1f77bcf86cd799439011"
        return {"message": "Subscribed successfully", "subscription_id": "sub123"}

    monkeypatch.setattr("app.controllers.subscription_controller.subscribe", fake_subscribe)

    response = client.post(
        "/subscriptions/",
        json={"plan_id": "507f1f77bcf86cd799439011"},
        headers=auth_header("customer"),
    )

    assert response.status_code == 200
    assert response.json()["subscription_id"] == "sub123"


def test_access_endpoint_and_history_work_with_token(monkeypatch):
    def fake_access_content(user_id, content_id):
        assert user_id == "user-1"
        assert content_id == "507f1f77bcf86cd799439012"
        return {"message": "Access granted", "log_id": "log123"}

    def fake_get_access_history(user_id):
        assert user_id == "user-1"
        return [{"_id": "log123", "content_id": "507f1f77bcf86cd799439012", "watched_at": "2026-04-04T10:00:00"}]

    monkeypatch.setattr("app.controllers.access_controller.access_content", fake_access_content)
    monkeypatch.setattr("app.controllers.access_controller.get_access_history", fake_get_access_history)

    access_response = client.post("/access/507f1f77bcf86cd799439012", headers=auth_header("customer"))
    history_response = client.get("/access/history", headers=auth_header("customer"))

    assert access_response.status_code == 200
    assert access_response.json()["log_id"] == "log123"
    assert history_response.status_code == 200
    assert history_response.json()[0]["_id"] == "log123"

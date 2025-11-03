"""Additional tests for Rules API to reach ≥90% coverage."""

from __future__ import annotations

from web.extensions import db
from web.models import Rule, User


def test_list_rules_with_section_filter(client, app):
    """Test listing rules with section filter."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(name="Rule1", content="Content1", section="naming")
        rule2 = Rule(name="Rule2", content="Content2", section="packaging")
        db.session.add_all([rule1, rule2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/rules?section=naming", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all(r["section"] == "naming" for r in data["rules"])


def test_list_rules_with_year_filter(client, app):
    """Test listing rules with year filter."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(name="Rule1", content="Content1", year=2022)
        rule2 = Rule(name="Rule2", content="Content2", year=2023)
        db.session.add_all([rule1, rule2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/rules?year=2022", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all(r["year"] == 2022 for r in data["rules"])


def test_get_rule_not_found(client, app):
    """Test getting non-existent rule."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/rules/99999", headers=headers)
        assert response.status_code == 404


def test_create_rule_missing_fields(client, app):
    """Test creating rule with missing required fields."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Missing name
        response = client.post(
            "/api/rules",
            json={"content": "Content"},
            headers=headers,
        )
        assert response.status_code == 400

        # Missing content
        response = client.post(
            "/api/rules",
            json={"name": "Rule"},
            headers=headers,
        )
        assert response.status_code == 400


def test_create_rule_no_data(client, app):
    """Test creating rule with no data."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = client.post("/api/rules", json={}, headers=headers)
        assert response.status_code == 400


def test_update_rule_not_found(client, app):
    """Test updating non-existent rule."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            "/api/rules/99999",
            json={"name": "Updated"},
            headers=headers,
        )
        assert response.status_code == 404


def test_update_rule_no_data(client, app):
    """Test updating rule with no data."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule = Rule(name="Rule1", content="Content1")
        db.session.add(rule)
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = client.put(
            f"/api/rules/{rule_id}",
            json={},
            headers=headers,
        )
        assert response.status_code == 400


def test_update_rule_all_fields(client, app):
    """Test updating rule with all fields."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule = Rule(name="Rule1", content="Content1")
        db.session.add(rule)
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/rules/{rule_id}",
            json={
                "name": "Updated",
                "content": "Updated Content",
                "scene": "EBOOK",
                "section": "naming",
                "year": 2023,
            },
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["rule"]["name"] == "Updated"
        assert data["rule"]["scene"] == "EBOOK"
        assert data["rule"]["year"] == 2023


def test_delete_rule_not_found(client, app):
    """Test deleting non-existent rule."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete("/api/rules/99999", headers=headers)
        assert response.status_code == 404

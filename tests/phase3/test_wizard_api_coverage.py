"""Additional tests for Wizard API to reach ≥90% coverage."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Rule, User


def test_create_draft_user_not_found_missing_id(client, app):
    """Test create_draft when current_user_id is None (edge case)."""
    # This tests line 30 - but JWT should always provide a user_id
    # We'll test with invalid token instead
    response = client.post(
        "/api/wizard/draft",
        headers={"Authorization": "Bearer invalid_token"},
        json={"group": "TestGroup", "release_type": "EBOOK", "rule_id": 1},
    )
    # Should return 401 or 422 (invalid token)
    assert response.status_code in [401, 422]


def test_create_draft_user_not_found(client, app):
    """Test create_draft when user not found."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule = Rule(name="TestRule", content="Content", section="eBOOK")
        db.session.add(rule)
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user (simulate user deleted after token issued)
        db.session.delete(user)
        db.session.commit()

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"group": "TestGroup", "release_type": "EBOOK", "rule_id": rule_id},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_create_draft_missing_group(client, app):
    """Test create_draft with missing group."""
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

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"release_type": "EBOOK", "rule_id": 1},
        )
        assert response.status_code == 400
        assert "group" in response.get_json()["message"].lower()


def test_create_draft_missing_release_type(client, app):
    """Test create_draft with missing release_type."""
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

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"group": "TestGroup", "rule_id": 1},
        )
        assert response.status_code == 400
        assert "release type" in response.get_json()["message"].lower()


def test_create_draft_missing_rule_id(client, app):
    """Test create_draft with missing rule_id."""
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

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"group": "TestGroup", "release_type": "EBOOK"},
        )
        assert response.status_code == 400
        assert "rule id" in response.get_json()["message"].lower()


def test_create_draft_empty_group_name(client, app):
    """Test create_draft with empty group name."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule = Rule(name="TestRule", content="Content", section="eBOOK")
        db.session.add(rule)
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"group": "   ", "release_type": "EBOOK", "rule_id": rule_id},
        )
        assert response.status_code == 400
        assert "group name cannot be empty" in response.get_json()["message"].lower()


def test_create_draft_success_new_group(client, app):
    """Test create_draft success with new group."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule = Rule(name="TestRule", content="Content", section="eBOOK")
        db.session.add(rule)
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={"group": "NewGroup", "release_type": "EBOOK", "rule_id": rule_id},
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "release_id" in data
        assert "job_id" in data
        assert "message" in data


def test_create_draft_success_existing_group(client, app):
    """Test create_draft success with existing group."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        group = Group(name="ExistingGroup")
        rule = Rule(name="TestRule", content="Content", section="eBOOK")
        db.session.add_all([group, rule])
        db.session.commit()
        rule_id = rule.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            "/api/wizard/draft",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "group": "ExistingGroup",
                "release_type": "EBOOK",
                "rule_id": rule_id,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "release_id" in data
        assert "job_id" in data


def test_list_rules_with_release_type(client, app):
    """Test list_rules with release_type filter."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(name="EBookRule", content="Content", section="eBOOK")
        rule2 = Rule(name="TVRule", content="Content", section="TV-720p")
        db.session.add_all([rule1, rule2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.get(
            "/api/wizard/rules?release_type=EBOOK",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "rules" in data
        assert len(data["rules"]) >= 1


def test_list_rules_with_tv_release_type(client, app):
    """Test list_rules with TV release_type filter."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(name="TVRule720p", content="Content", section="TV-720p")
        rule2 = Rule(name="TVRuleSD", content="Content", section="TV-SD")
        rule3 = Rule(name="EBookRule", content="Content", section="eBOOK")
        db.session.add_all([rule1, rule2, rule3])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.get(
            "/api/wizard/rules?release_type=TV",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "rules" in data
        assert len(data["rules"]) >= 2

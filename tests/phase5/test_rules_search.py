"""Tests for Rules API search functionality."""

from __future__ import annotations

from web.extensions import db
from web.models import Rule, User


def test_list_rules_with_search(client, app):
    """Test list_rules with search parameter."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(
            name="EBook Rule 2022",
            content="This is an eBook rule content",
            section="eBOOK",
            year=2022,
        )
        rule2 = Rule(
            name="TV Rule 2023",
            content="This is a TV rule content",
            section="TV-720p",
            year=2023,
        )
        rule3 = Rule(
            name="EBook Rule 2023",
            content="Another eBook rule",
            section="eBOOK",
            year=2023,
        )
        db.session.add_all([rule1, rule2, rule3])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Search for "EBook"
        response = client.get(
            "/api/rules?search=EBook",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["rules"]) == 2
        assert all("EBook" in rule["name"] for rule in data["rules"])

        # Search in content
        response = client.get(
            "/api/rules?search=TV rule",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["rules"]) == 1
        assert "TV" in data["rules"][0]["name"]


def test_list_rules_with_search_and_filters(client, app):
    """Test list_rules with search and filters combined."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        rule1 = Rule(
            name="EBook Rule 2022",
            content="Content",
            section="eBOOK",
            year=2022,
        )
        rule2 = Rule(
            name="EBook Rule 2023",
            content="Content",
            section="eBOOK",
            year=2023,
        )
        rule3 = Rule(
            name="TV Rule 2022",
            content="Content",
            section="TV-720p",
            year=2022,
        )
        db.session.add_all([rule1, rule2, rule3])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Search + year filter
        response = client.get(
            "/api/rules?search=EBook&year=2022",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["rules"]) == 1
        assert data["rules"][0]["name"] == "EBook Rule 2022"

        # Search + section filter
        response = client.get(
            "/api/rules?search=Rule&section=eBOOK",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["rules"]) == 2
        assert all(rule["section"] == "eBOOK" for rule in data["rules"])


def test_list_rules_search_empty_result(client, app):
    """Test list_rules with search returning no results."""
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

        response = client.get(
            "/api/rules?search=NonexistentRule",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["rules"]) == 0
        assert data["pagination"]["total"] == 0

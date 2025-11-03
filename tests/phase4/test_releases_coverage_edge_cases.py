"""Edge case tests for releases.py to reach ≥90% coverage."""

from __future__ import annotations

import pytest
from flask import Flask

from web.extensions import db
from web.models import Release, User


def test_list_releases_empty_result(client, app):
    """Test list_releases with no releases."""
    with app.app_context():
        # Create user and login
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
        
        response = client.get("/api/releases", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["releases"] == []
        assert data["pagination"]["total"] == 0


def test_list_releases_zero_per_page(client, app):
    """Test list_releases with per_page=0 (should use default)."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?per_page=0",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        # Should use default per_page (20)
        assert data["pagination"]["per_page"] == 20


def test_list_releases_negative_page(client, app):
    """Test list_releases with negative page number."""
    with app.app_context():
        # Create user and login
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
        
        response = client.get("/api/releases?page=-1", headers=headers)
        assert response.status_code == 200
        # Should handle gracefully (use page 1 or return empty)


def test_list_releases_large_page_number(client, app):
    """Test list_releases with very large page number."""
    with app.app_context():
        # Create user and login
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
        
        response = client.get("/api/releases?page=99999", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        # Should return empty results
        assert data["releases"] == []


def test_get_release_user_id_none(client, app):
    """Test get_release normal case (covers line 140)."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id
        
        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Normal case should work (covers line 140: return release.to_dict())
        response = client.get(
            f"/api/releases/{release_id}",
            headers=headers,
        )
        assert response.status_code == 200
        assert "release" in response.get_json()


def test_update_release_empty_metadata(client, app):
    """Test update_release with empty metadata."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/releases/{release_id}",
            json={"release_metadata": {}},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "release" in data
        release_data = data["release"]
        # to_dict() always includes release_metadata (defaults to {})
        assert release_data["release_metadata"] == {}


def test_update_release_empty_config(client, app):
    """Test update_release with empty config."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/releases/{release_id}",
            json={"config": {}},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "release" in data
        release_data = data["release"]
        # to_dict() always includes config (defaults to {})
        assert release_data["config"] == {}

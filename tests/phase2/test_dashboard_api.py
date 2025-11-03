"""Tests for Dashboard API."""

from __future__ import annotations

from web.extensions import db
from web.models import Job, Release, User


def test_get_stats_user_not_found(client, app):
    """Test get_stats when user not found."""
    with app.app_context():
        # Create a user and get token
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user (simulate user deleted after token issued)
        db.session.delete(user)
        db.session.commit()

        # Try to get stats with valid token but deleted user
        response = client.get(
            "/api/dashboard/stats",
            headers={"Authorization": f"Bearer {token}"},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_get_stats_success(client, app):
    """Test get_stats success."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Create some releases and jobs
        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        release2 = Release(
            user_id=user.id,
            release_type="TV",
            status="draft",
            release_metadata={},
        )
        job1 = Job(
            release_id=release1.id,
            created_by=user.id,
            status="completed",
            config_json={},
        )
        db.session.add_all([release1, release2, job1])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.get(
            "/api/dashboard/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "total_releases" in data
        assert "total_jobs" in data
        assert "user_releases" in data
        assert "user_jobs" in data
        assert "user" in data
        assert data["user_releases"] >= 2
        assert data["user_jobs"] >= 1

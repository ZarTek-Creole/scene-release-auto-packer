"""Tests for Dashboard component (Phase 2 - Frontend testing via API validation)."""

from __future__ import annotations

from web.extensions import db
from web.models import User


def test_dashboard_stats_user_not_found(client, auth_headers) -> None:
    """Test dashboard stats when user not found."""
    # Create a user and login
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Delete user
    with client.application.app_context():
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

    # Try to get dashboard stats with deleted user token
    response = client.get(
        "/api/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should return 404 or 401
    assert response.status_code in [401, 404]


def test_dashboard_stats_empty(client, auth_headers) -> None:
    """Test dashboard stats with no data."""
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Get dashboard stats
    response = client.get(
        "/api/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["total_releases"] == 0
    assert data["total_jobs"] == 0
    assert data["user_releases"] == 0
    assert data["user_jobs"] == 0
    assert "user" in data

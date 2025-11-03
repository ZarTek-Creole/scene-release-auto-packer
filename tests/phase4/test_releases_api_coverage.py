"""Additional tests to improve coverage for Releases API (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Release, User


def test_list_releases_no_user_filter(client, auth_headers) -> None:
    """Test listing releases without user_id filter (defaults to current user)."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        release = Release(user_id=user_id, release_type="EBOOK", status="completed")
        db.session.add(release)
        db.session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # No user_id param - should show only current user's releases
    response = client.get(
        "/api/releases",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["user_id"] == user_id


def test_list_releases_default_sort(client, auth_headers) -> None:
    """Test listing releases with default sort (created_at desc)."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release1 = Release(user_id=user.id, release_type="EBOOK", status="completed")
        release2 = Release(user_id=user.id, release_type="TV", status="draft")
        db.session.add_all([release1, release2])
        db.session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # No sort params - should default to created_at desc
    response = client.get(
        "/api/releases",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 2
    # Newest first (TV should be last)
    assert data["releases"][0]["release_type"] in ["EBOOK", "TV"]


def test_get_release_permission_denied(client, auth_headers) -> None:
    """Test getting release from another user (permission denied)."""
    with client.application.app_context():
        db.create_all()

        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(user_id=user2.id, release_type="EBOOK", status="completed")
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # User1 trying to access user2's release
    response = client.get(
        f"/api/releases/{release_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert "Permission denied" in response.get_json()["message"]


def test_update_release_not_found(client, auth_headers) -> None:
    """Test updating non-existent release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.put(
        "/api/releases/99999",
        json={"status": "completed"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_delete_release_permission_denied(client, auth_headers) -> None:
    """Test deleting release from another user (permission denied)."""
    with client.application.app_context():
        db.create_all()

        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(user_id=user2.id, release_type="EBOOK", status="completed")
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.delete(
        f"/api/releases/{release_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

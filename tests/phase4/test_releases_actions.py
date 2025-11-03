"""Tests for Releases Actions API endpoints (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Release, User


def test_nfofix_action(client, auth_headers) -> None:
    """Test NFOFIX action on a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"nfo_content": "invalid nfo"},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.post(
        f"/api/releases/{release_id}/actions/nfofix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "job_id" in data


def test_readnfo_action(client, auth_headers) -> None:
    """Test READNFO action on a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            file_path="/path/to/release.nfo",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.post(
        f"/api/releases/{release_id}/actions/readnfo",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "job_id" in data


def test_repack_action(client, auth_headers) -> None:
    """Test REPACK action on a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            config={"zip_size": 50},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.post(
        f"/api/releases/{release_id}/actions/repack",
        json={"zip_size": 100},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "job_id" in data


def test_dirfix_action(client, auth_headers) -> None:
    """Test DIRFIX action on a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            file_path="/path/to/release",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.post(
        f"/api/releases/{release_id}/actions/dirfix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "job_id" in data


def test_action_permission_denied(client, auth_headers) -> None:
    """Test action on release from another user (permission denied)."""
    with client.application.app_context():
        db.create_all()

        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(
            user_id=user2.id,
            release_type="EBOOK",
            status="completed",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.post(
        f"/api/releases/{release_id}/actions/nfofix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

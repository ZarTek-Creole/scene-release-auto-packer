"""Tests for release update endpoint (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Release, User


def test_update_release(client, auth_headers) -> None:
    """Test updating a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.commit()

        release = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="draft",
            release_metadata={"title": "Old Title"},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Update release
    response = client.put(
        f"/api/releases/{release_id}",
        json={
            "release_metadata": {"title": "New Title", "author": "New Author"},
            "status": "completed",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "release" in data
    assert data["release"]["status"] == "completed"
    assert data["release"]["release_metadata"]["title"] == "New Title"

    # Verify update persisted
    with client.application.app_context():
        updated_release = Release.query.get(release_id)
        assert updated_release.status == "completed"
        assert updated_release.release_metadata["title"] == "New Title"


def test_update_release_permission_denied(client, auth_headers) -> None:
    """Test updating release without permission."""
    with client.application.app_context():
        db.create_all()

        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add_all([user1, user2])
        db.session.commit()

        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.commit()

        release = Release(
            user_id=user1.id,
            group_id=group.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    # Login as user2
    login_response = client.post(
        "/api/auth/login",
        json={"username": "user2", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Try to update release owned by user1
    response = client.put(
        f"/api/releases/{release_id}",
        json={"status": "completed"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert "permission denied" in response.get_json()["message"].lower()

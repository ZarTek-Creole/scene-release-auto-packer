"""Tests for releases actions endpoints (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Job, Release, User


def test_nfofix_action(client, auth_headers) -> None:
    """Test NFOFIX action."""
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
            status="completed",
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

    # Execute NFOFIX action
    response = client.post(
        f"/api/releases/{release_id}/actions/nfofix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "nfofix" in data["message"].lower()

    # Verify job was created
    with client.application.app_context():
        job = Job.query.filter_by(release_id=release_id).first()
        assert job is not None
        assert job.config_json["action"] == "nfofix"


def test_readnfo_action(client, auth_headers) -> None:
    """Test READNFO action."""
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
            status="completed",
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

    # Execute READNFO action
    response = client.post(
        f"/api/releases/{release_id}/actions/readnfo",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "readnfo" in data["message"].lower()


def test_repack_action(client, auth_headers) -> None:
    """Test REPACK action."""
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
            status="completed",
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

    # Execute REPACK action
    response = client.post(
        f"/api/releases/{release_id}/actions/repack",
        json={"config": {"compression": "max"}},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "repack" in data["message"].lower()


def test_dirfix_action(client, auth_headers) -> None:
    """Test DIRFIX action."""
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
            status="completed",
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

    # Execute DIRFIX action
    response = client.post(
        f"/api/releases/{release_id}/actions/dirfix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    data = response.get_json()
    assert "job_id" in data
    assert "dirfix" in data["message"].lower()


def test_action_permission_denied(client, auth_headers) -> None:
    """Test action without permission."""
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
            status="completed",
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

    # Try to execute action on release owned by user1
    response = client.post(
        f"/api/releases/{release_id}/actions/nfofix",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert "permission denied" in response.get_json()["message"].lower()

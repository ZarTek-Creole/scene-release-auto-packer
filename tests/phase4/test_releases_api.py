"""Tests for Releases API endpoints (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Release, User


def test_list_releases_with_search(client, auth_headers) -> None:
    """Test listing releases with search query."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"title": "Test Book 1"},
        )
        release2 = Release(
            user_id=user.id,
            release_type="TV",
            status="draft",
            release_metadata={"title": "Another Book"},
        )
        db.session.add_all([release1, release2])
        db.session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.get(
        "/api/releases?search=Test",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["release_type"] == "EBOOK"


def test_list_releases_with_sort(client, auth_headers) -> None:
    """Test listing releases with sorting."""
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

    response = client.get(
        "/api/releases?sort_by=release_type&sort_order=asc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 2
    assert data["releases"][0]["release_type"] == "EBOOK"


def test_update_release(client, auth_headers) -> None:
    """Test updating a release."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
            release_metadata={"title": "Original Title"},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.put(
        f"/api/releases/{release_id}",
        json={"release_metadata": {"title": "Updated Title"}},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["release"]["release_metadata"]["title"] == "Updated Title"

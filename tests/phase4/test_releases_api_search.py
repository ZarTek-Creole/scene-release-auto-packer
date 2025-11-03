"""Tests for release search functionality (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Release, User


def test_search_releases_by_title(client, auth_headers) -> None:
    """Test searching releases by title."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.commit()

        release1 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"title": "Test Book", "author": "Author One"},
        )
        release2 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"title": "Another Book", "author": "Author Two"},
        )
        db.session.add_all([release1, release2])
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Search by title
    response = client.get(
        "/api/releases?search=Test",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert "Test" in data["releases"][0]["release_metadata"]["title"]


def test_search_releases_by_author(client, auth_headers) -> None:
    """Test searching releases by author."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.commit()

        release1 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"title": "Book One", "author": "Test Author"},
        )
        release2 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={"title": "Book Two", "author": "Other Author"},
        )
        db.session.add_all([release1, release2])
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Search by author
    response = client.get(
        "/api/releases?search=Test Author",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["release_metadata"]["author"] == "Test Author"


def test_list_releases_sort_by_type(client, auth_headers) -> None:
    """Test sorting releases by type."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.commit()

        release1 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="TV",
            status="completed",
        )
        release2 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="completed",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Sort by type ascending
    response = client.get(
        "/api/releases?sort_by=release_type&sort_order=asc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 2
    # EBOOK should come before TV alphabetically
    assert data["releases"][0]["release_type"] == "EBOOK"
    assert data["releases"][1]["release_type"] == "TV"

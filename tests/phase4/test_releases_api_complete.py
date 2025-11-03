"""Complete tests for releases API (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Release, User


def test_list_releases_combined_filters(client, auth_headers) -> None:
    """Test combining multiple filters."""
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
        )
        release2 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="draft",
        )
        release3 = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="TV",
            status="completed",
        )
        db.session.add_all([release1, release2, release3])
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Filter by type and status
    response = client.get(
        "/api/releases?release_type=EBOOK&status=completed",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["release_type"] == "EBOOK"
    assert data["releases"][0]["status"] == "completed"


def test_list_releases_filter_by_group(client, auth_headers) -> None:
    """Test filtering releases by group ID."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        group1 = Group(name="Group1")
        group2 = Group(name="Group2")
        db.session.add_all([group1, group2])
        db.session.commit()

        release1 = Release(
            user_id=user.id,
            group_id=group1.id,
            release_type="EBOOK",
            status="completed",
        )
        release2 = Release(
            user_id=user.id,
            group_id=group2.id,
            release_type="EBOOK",
            status="completed",
        )
        db.session.add_all([release1, release2])
        db.session.commit()
        group1_id = group1.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Filter by group
    response = client.get(
        f"/api/releases?group_id={group1_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["group_id"] == group1_id


def test_update_release_partial(client, auth_headers) -> None:
    """Test partial update of release."""
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
            release_metadata={"title": "Original Title"},
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

    # Update only status
    response = client.put(
        f"/api/releases/{release_id}",
        json={"status": "completed"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["release"]["status"] == "completed"
    # Metadata should remain unchanged
    assert data["release"]["release_metadata"]["title"] == "Original Title"

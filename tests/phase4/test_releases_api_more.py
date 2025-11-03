"""Additional tests for Releases API (Phase 4)."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Release, User


def test_list_releases_pagination(client, auth_headers) -> None:
    """Test pagination for releases list."""
    with client.application.app_context():
        db.create_all()

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # Create 25 releases
        for _i in range(25):
            release = Release(
                user_id=user.id,
                release_type="EBOOK",
                status="completed",
            )
            db.session.add(release)
        db.session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # First page
    response = client.get(
        "/api/releases?page=1&per_page=20",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 20
    assert data["pagination"]["total"] == 25
    assert data["pagination"]["pages"] == 2

    # Second page
    response = client.get(
        "/api/releases?page=2&per_page=20",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 5


def test_list_releases_group_filter(client, auth_headers) -> None:
    """Test filtering releases by group."""
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
            user_id=user.id, group_id=group2.id, release_type="TV", status="completed"
        )
        db.session.add_all([release1, release2])
        db.session.commit()
        group1_id = group1.id

    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    response = client.get(
        f"/api/releases?group_id={group1_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["releases"]) == 1
    assert data["releases"][0]["group_id"] == group1_id

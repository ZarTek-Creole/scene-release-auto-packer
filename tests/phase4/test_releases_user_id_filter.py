"""Test user_id filter in list_releases (covers line 63)."""

from __future__ import annotations

from web.extensions import db
from web.models import Release, User


def test_list_releases_with_user_id_filter(client, app):
    """Test list_releases with user_id filter (covers line 63)."""
    with app.app_context():
        # Create user1
        user1 = User(username="user1", email="user1@test.com")
        user1.set_password("password")
        db.session.add(user1)
        db.session.flush()
        
        # Create user2
        user2 = User(username="user2", email="user2@test.com")
        user2.set_password("password")
        db.session.add(user2)
        db.session.flush()

        # Create releases for both users
        release1 = Release(
            user_id=user1.id,
            release_type="EBOOK",
            status="draft",
        )
        release2 = Release(
            user_id=user2.id,
            release_type="TV",
            status="completed",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

        # Login as user1
        login_response = client.post(
            "/api/auth/login",
            json={"username": "user1", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Filter by user1's ID (should only return user1's releases)
        response = client.get(
            f"/api/releases?user_id={user1.id}",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        # Should only return user1's releases
        for release in data["releases"]:
            assert release["user_id"] == user1.id

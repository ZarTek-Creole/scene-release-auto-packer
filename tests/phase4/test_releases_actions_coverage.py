"""Additional tests for Releases Actions API to reach ?90% coverage."""

from __future__ import annotations

from web.extensions import db
from web.models import Group, Release, User


def test_nfofix_release_user_not_found(client, app):
    """Test nfofix_release when user not found."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user and release (simulate user deleted after token issued)
        # Delete release first to avoid foreign key constraint
        release = db.session.get(Release, release_id)
        if release:
            db.session.delete(release)
        # Then delete user
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
        db.session.commit()

        response = client.post(
            f"/api/releases/{release_id}/actions/nfofix",
            headers={"Authorization": f"Bearer {token}"},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_readnfo_release_user_not_found(client, app):
    """Test readnfo_release when user not found."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
            file_path="/path/to/file.epub",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user and release (simulate user deleted after token issued)
        # Delete release first to avoid foreign key constraint
        release = db.session.get(Release, release_id)
        if release:
            db.session.delete(release)
        # Then delete user
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
        db.session.commit()

        response = client.post(
            f"/api/releases/{release_id}/actions/readnfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_readnfo_release_permission_denied(client, app):
    """Test readnfo_release when permission denied (other user's release)."""
    with app.app_context():
        user1 = User(username="user1", email="user1@test.com")
        user1.set_password("password")
        user2 = User(username="user2", email="user2@test.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(
            user_id=user1.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
            file_path="/path/to/file.epub",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "user2", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            f"/api/releases/{release_id}/actions/readnfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "permission denied" in response.get_json()["message"].lower()


def test_repack_release_user_not_found(client, app):
    """Test repack_release when user not found."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user and release (simulate user deleted after token issued)
        # Delete release first to avoid foreign key constraint
        release = db.session.get(Release, release_id)
        if release:
            db.session.delete(release)
        # Then delete user
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
        db.session.commit()

        response = client.post(
            f"/api/releases/{release_id}/actions/repack",
            headers={"Authorization": f"Bearer {token}"},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_repack_release_permission_denied(client, app):
    """Test repack_release when permission denied (other user's release)."""
    with app.app_context():
        user1 = User(username="user1", email="user1@test.com")
        user1.set_password("password")
        user2 = User(username="user2", email="user2@test.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(
            user_id=user1.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "user2", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            f"/api/releases/{release_id}/actions/repack",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "permission denied" in response.get_json()["message"].lower()


def test_dirfix_release_user_not_found(client, app):
    """Test dirfix_release when user not found."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        # Delete user and release (simulate user deleted after token issued)
        # Delete release first to avoid foreign key constraint
        release = db.session.get(Release, release_id)
        if release:
            db.session.delete(release)
        # Then delete user
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
        db.session.commit()

        response = client.post(
            f"/api/releases/{release_id}/actions/dirfix",
            headers={"Authorization": f"Bearer {token}"},
        )
        # JWT might validate first (401) or endpoint checks user (404)
        assert response.status_code in [401, 404]
        if response.status_code == 404:
            assert "user not found" in response.get_json()["message"].lower()


def test_dirfix_release_permission_denied(client, app):
    """Test dirfix_release when permission denied (other user's release)."""
    with app.app_context():
        user1 = User(username="user1", email="user1@test.com")
        user1.set_password("password")
        user2 = User(username="user2", email="user2@test.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        release = Release(
            user_id=user1.id,
            release_type="EBOOK",
            status="completed",
            release_metadata={},
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "user2", "password": "password"},
        )
        token = login_response.get_json()["access_token"]

        response = client.post(
            f"/api/releases/{release_id}/actions/dirfix",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "permission denied" in response.get_json()["message"].lower()

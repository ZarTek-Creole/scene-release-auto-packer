"""Test delete_release commit path (covers lines 210-213)."""

from __future__ import annotations

from web.extensions import db
from web.models import Release, User


def test_delete_release_success(client, app):
    """Test successful delete_release (covers lines 210-213)."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        release_id = release.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Delete release (covers lines 210-213: delete, commit, return)
        response = client.delete(
            f"/api/releases/{release_id}",
            headers=headers,
        )
        assert response.status_code == 200
        assert "deleted successfully" in response.get_json()["message"].lower()
        
        # Verify release is deleted
        deleted_release = db.session.get(Release, release_id)
        assert deleted_release is None

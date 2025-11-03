"""Complete sort tests for releases.py to cover all sort branches."""

from __future__ import annotations

import pytest
from flask import Flask

from web.extensions import db
from web.models import Release, User


def test_list_releases_sort_created_at_asc(client, app):
    """Test list_releases sort by created_at ascending."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        # Create releases with different timestamps
        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release1)
        db.session.flush()
        
        release2 = Release(
            user_id=user.id,
            release_type="TV",
            status="completed",
        )
        db.session.add(release2)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?sort_by=created_at&sort_order=asc",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["releases"]) >= 2
        # Verify ascending order (older first)
        releases = data["releases"]
        for i in range(len(releases) - 1):
            assert releases[i]["id"] <= releases[i + 1]["id"]


def test_list_releases_sort_release_type_asc(client, app):
    """Test list_releases sort by release_type ascending."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release1 = Release(
            user_id=user.id,
            release_type="TV",
            status="draft",
        )
        release2 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?sort_by=release_type&sort_order=asc",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        releases = data["releases"]
        # Find our test releases
        test_releases = [r for r in releases if r["id"] in [release1.id, release2.id]]
        if len(test_releases) == 2:
            # EBOOK should come before TV alphabetically
            assert test_releases[0]["release_type"] == "EBOOK"
            assert test_releases[1]["release_type"] == "TV"


def test_list_releases_sort_release_type_desc(client, app):
    """Test list_releases sort by release_type descending."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        release2 = Release(
            user_id=user.id,
            release_type="TV",
            status="draft",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?sort_by=release_type&sort_order=desc",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        releases = data["releases"]
        # Find our test releases
        test_releases = [r for r in releases if r["id"] in [release1.id, release2.id]]
        if len(test_releases) == 2:
            # TV should come before EBOOK alphabetically (desc)
            assert test_releases[0]["release_type"] == "TV"
            assert test_releases[1]["release_type"] == "EBOOK"


def test_list_releases_sort_status_asc(client, app):
    """Test list_releases sort by status ascending."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
        )
        release2 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?sort_by=status&sort_order=asc",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        releases = data["releases"]
        # Find our test releases
        test_releases = [r for r in releases if r["id"] in [release1.id, release2.id]]
        if len(test_releases) == 2:
            # "completed" should come before "draft" alphabetically
            assert test_releases[0]["status"] == "completed"
            assert test_releases[1]["status"] == "draft"


def test_list_releases_sort_status_desc(client, app):
    """Test list_releases sort by status descending."""
    with app.app_context():
        # Create user and login
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        release1 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="draft",
        )
        release2 = Release(
            user_id=user.id,
            release_type="EBOOK",
            status="completed",
        )
        db.session.add_all([release1, release2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/releases?sort_by=status&sort_order=desc",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        releases = data["releases"]
        # Find our test releases
        test_releases = [r for r in releases if r["id"] in [release1.id, release2.id]]
        if len(test_releases) == 2:
            # "draft" should come before "completed" alphabetically (desc)
            assert test_releases[0]["status"] == "draft"
            assert test_releases[1]["status"] == "completed"

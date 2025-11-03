"""Tests for Rules API upload functionality."""

from __future__ import annotations

from io import BytesIO

from web.extensions import db
from web.models import Rule, User


def test_upload_rule_success(client, app):
    """Test upload_rule success."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create test file
        file_content = """[2022] eBOOK Rules
Section: eBOOK
Scene: English

Content of the rule here.
"""
        file_data = BytesIO(file_content.encode("utf-8"))
        file_data.name = "ebook_rule_2022.nfo"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "ebook_rule_2022.nfo"),
                "name": "EBook Rule 2022",
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "rule" in data
        assert data["rule"]["name"] == "EBook Rule 2022"
        assert "eBOOK" in data["rule"]["content"]
        assert "metadata_extracted" in data


def test_upload_rule_extract_metadata(client, app):
    """Test upload_rule with metadata extraction."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create test file with metadata in content
        file_content = """[English Scene]
[2022] eBOOK Rules
Section: eBOOK

Content here.
"""
        file_data = BytesIO(file_content.encode("utf-8"))
        file_data.name = "rule.nfo"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "rule.nfo"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "metadata_extracted" in data
        # Metadata should be extracted
        metadata = data["metadata_extracted"]
        assert metadata["section"] == "eBOOK" or metadata["year"] == 2022


def test_upload_rule_no_file(client, app):
    """Test upload_rule with no file."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={},
        )

        assert response.status_code == 400
        assert "no file provided" in response.get_json()["message"].lower()


def test_upload_rule_invalid_extension(client, app):
    """Test upload_rule with invalid file extension."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        file_data = BytesIO(b"test content")
        file_data.name = "rule.pdf"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "rule.pdf"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        assert "invalid file type" in response.get_json()["message"].lower()


def test_upload_rule_with_manual_metadata(client, app):
    """Test upload_rule with manual metadata override."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        file_content = "Rule content here."
        file_data = BytesIO(file_content.encode("utf-8"))
        file_data.name = "rule.nfo"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "rule.nfo"),
                "name": "Custom Rule Name",
                "scene": "French",
                "section": "TV-720p",
                "year": "2023",
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["rule"]["name"] == "Custom Rule Name"
        assert data["rule"]["scene"] == "French"
        assert data["rule"]["section"] == "TV-720p"
        assert data["rule"]["year"] == 2023

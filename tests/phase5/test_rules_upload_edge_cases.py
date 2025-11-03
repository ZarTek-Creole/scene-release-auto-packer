"""Additional edge case tests for Rules API upload functionality."""

from __future__ import annotations

from io import BytesIO

from web.extensions import db
from web.models import Rule, User


def test_upload_rule_empty_filename(client, app):
    """Test upload_rule with empty filename."""
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
        file_data.name = ""

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, ""),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        assert "no file selected" in response.get_json()["message"].lower()


def test_upload_rule_invalid_encoding(client, app):
    """Test upload_rule with invalid encoding."""
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

        # Create file with invalid encoding (binary data)
        file_data = BytesIO(b"\xff\xfe\x00\x01\x02\x03")
        file_data.name = "rule.nfo"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "rule.nfo"),
            },
            content_type="multipart/form-data",
        )

        # Should handle encoding error gracefully
        assert response.status_code in [400, 201]  # May succeed with ISO-8859-1


def test_upload_rule_txt_extension(client, app):
    """Test upload_rule with .txt extension."""
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

        file_content = "Rule content in TXT format."
        file_data = BytesIO(file_content.encode("utf-8"))
        file_data.name = "rule.txt"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "rule.txt"),
                "name": "TXT Rule",
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["rule"]["name"] == "TXT Rule"


def test_upload_rule_filename_as_name(client, app):
    """Test upload_rule using filename as name when name not provided."""
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

        file_content = "Rule content."
        file_data = BytesIO(file_content.encode("utf-8"))
        file_data.name = "my_custom_rule.nfo"

        response = client.post(
            "/api/rules/upload",
            headers=headers,
            data={
                "file": (file_data, "my_custom_rule.nfo"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201
        data = response.get_json()
        # Name should be extracted from filename (without extension)
        assert "my_custom_rule" in data["rule"]["name"].lower()

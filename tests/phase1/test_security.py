"""Tests for JWT security callbacks."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
from flask_jwt_extended import create_access_token

from web.extensions import db
from web.models import TokenBlocklist, User


def test_token_blocklist_check(client) -> None:
    """Test token blocklist check."""
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    access_token = login_response.get_json()["access_token"]

    # Decode token to get jti
    decoded = jwt.decode(
        access_token, options={"verify_signature": False}, algorithms=["HS256"]
    )
    jti = decoded.get("jti")

    # Decode to get exp
    exp = decoded.get("exp")
    expires_at = datetime.fromtimestamp(exp, tz=UTC) if exp else datetime.now(UTC)

    # Add token to blocklist
    with client.application.app_context():
        blocked_token = TokenBlocklist(
            jti=jti, token_type="access", expires_at=expires_at
        )
        db.session.add(blocked_token)
        db.session.commit()

    # Try to use blocked token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401


def test_expired_token_callback(client) -> None:
    """Test expired token callback."""
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # Store ID before session closes

    # Get user object within app context for token creation
    with client.application.app_context():
        user = User.query.get(user_id)
        expired_token = create_access_token(
            identity=user, expires_delta=timedelta(seconds=-1)
        )

    # Try to use expired token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
    data = response.get_json()
    assert (
        "expired" in data["message"].lower() or "Token has expired" in data["message"]
    )


def test_invalid_token_callback(client) -> None:
    """Test invalid token callback."""
    # Try to use invalid token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token_format"},
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid token" in data["message"] or "invalid" in data["message"].lower()


def test_missing_token_callback(client) -> None:
    """Test missing token callback."""
    # Try to access protected route without token
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    data = response.get_json()
    assert (
        "Authorization required" in data["message"]
        or "required" in data["message"].lower()
    )


def test_user_lookup_callback_inactive_user(client) -> None:
    """Test user lookup callback with inactive user."""
    with client.application.app_context():
        db.create_all()
        user = User(username="inactiveuser", email="inactive@example.com", active=False)
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login should fail for inactive user
    response = client.post(
        "/api/auth/login",
        json={"username": "inactiveuser", "password": "password123"},
    )

    assert response.status_code == 403
    data = response.get_json()
    assert "inactive" in data["message"].lower()
